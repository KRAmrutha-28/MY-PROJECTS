import os
import uuid
import logging
import sqlite3
import json
import re
import io
import base64
import traceback
from datetime import datetime
import threading

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, session, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your LLM module – make sure it's properly implemented
from llm_module import LLMModule
from config import Config

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'xlsm'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# LLM Module (try to initialize)
# ----------------------------------------------------------------------
llm_module = None
try:
    llm_module = LLMModule(api_key=Config.GEMINI_API_KEY)
    logger.info("✓ LLM Module initialized")
except Exception as e:
    logger.error(f"✗ LLM Module failed: {e}")

# ----------------------------------------------------------------------
# In‑memory data stores (per session)
# ----------------------------------------------------------------------
uploaded_data = {}      # session_id -> metadata + db_path + mappings
conversations = {}      # session_id -> list of Q/A pairs
data_lock = threading.Lock()

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_serializable(obj):
    """Convert numpy/pandas types to JSON‑serializable Python types."""
    if obj is None:
        return None
    if isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
        return int(obj)
    if isinstance(obj, (np.float64, np.float32, np.float16)):
        return None if np.isnan(obj) or np.isinf(obj) else float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, pd.Timestamp):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    if pd.isna(obj):
        return None
    return obj

def clean_column_name_for_sql(col_name):
    """Produce a safe SQL column name from the original (may still be weird)."""
    if not col_name or not str(col_name).strip():
        return 'column'
    s = str(col_name).strip()
    # Replace any non‑alphanumeric character with underscore
    s = re.sub(r'[^a-zA-Z0-9_]', '_', s)
    s = re.sub(r'_+', '_', s)
    if s and not s[0].isalpha() and s[0] != '_':
        s = 'col_' + s
    if len(s) > 50:
        s = s[:50]
    return s

def convert_to_numeric(df):
    """Try to convert string columns that look numeric."""
    converted = []
    for col in df.columns:
        try:
            sample = df[col].dropna().head(100)
            if len(sample) == 0:
                continue
            numeric_sample = pd.to_numeric(sample, errors='coerce')
            # if at least 80% can be converted, convert whole column
            if numeric_sample.notna().sum() / len(sample) >= 0.8:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                converted.append(col)
        except:
            pass
    return df, converted

def detect_column_type(series):
    """Return 'numeric', 'datetime', or 'categorical'."""
    if pd.api.types.is_numeric_dtype(series):
        return 'numeric'
    try:
        pd.to_datetime(series, errors='raise')
        return 'datetime'
    except:
        return 'categorical'

def read_csv_safe(file_path):
    """
    Try multiple encodings and separators to read a CSV.
    Returns (DataFrame, total_row_count_in_file)
    """
    # First, count total lines (estimate)
    total_rows = 0
    encodings_to_try = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    for enc in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                total_rows = sum(1 for _ in f) - 1  # subtract header
            break
        except:
            continue
    if total_rows == 0:
        total_rows = 50000  # fallback

    # Try reading with auto detection
    try:
        df = pd.read_csv(file_path, nrows=10000)
        if not df.empty and len(df.columns) > 0:
            logger.info("Read CSV with auto detection")
            return df, total_rows
    except Exception as e:
        logger.warning(f"Auto detection failed: {e}")

    # Try different encodings and separators
    separators = [',', ';', '\t', '|', ':']
    for enc in encodings_to_try:
        for sep in separators:
            try:
                df = pd.read_csv(file_path, encoding=enc, sep=sep, nrows=10000,
                                 on_bad_lines='skip')
                if not df.empty and len(df.columns) > 1:
                    logger.info(f"Read with encoding={enc}, sep={sep}")
                    return df, total_rows
            except:
                continue
    return None, 0

# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------
@app.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html', session_id=session['session_id'])

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        session_id = session.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id

        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400

        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{session_id}_{filename}")
        file.save(temp_path)

        try:
            if filename.endswith('.csv'):
                df, total_file_rows = read_csv_safe(temp_path)
            else:
                df = pd.read_excel(temp_path)
                total_file_rows = len(df)
                if len(df) > 10000:
                    df = df.head(10000)

            if df is None:
                return jsonify({'error': 'Could not read file'}), 400

            # Basic cleaning: remove completely empty columns/rows
            df = df.dropna(axis=1, how='all')
            df = df.dropna(how='all')
            if df.empty:
                return jsonify({'error': 'File contains no data'}), 400

            # 🔥 IMPORTANT: Preserve original column names exactly as they appear (strip whitespace only)
            df.columns = [str(col).strip() for col in df.columns]

            # Convert numeric columns
            df, converted_cols = convert_to_numeric(df)

            # Determine column types
            numeric_cols = []
            categorical_cols = []
            datetime_cols = []
            for col in df.columns:
                t = detect_column_type(df[col])
                if t == 'numeric':
                    numeric_cols.append(col)
                elif t == 'datetime':
                    datetime_cols.append(col)
                else:
                    categorical_cols.append(col)

            display_rows = len(df)
            logger.info(f"Uploaded: {display_rows} rows, columns: {list(df.columns)}")

            # Create SQL‑safe column names for the database (mapping)
            column_mapping = {}
            reverse_mapping = {}
            for col in df.columns:
                sql_col = clean_column_name_for_sql(col)
                orig = sql_col
                cnt = 1
                while sql_col in column_mapping.values():
                    sql_col = f"{orig}_{cnt}"
                    cnt += 1
                column_mapping[col] = sql_col
                reverse_mapping[sql_col] = col

            # SQLite database
            db_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}.db")
            if os.path.exists(db_path):
                os.remove(db_path)

            conn = sqlite3.connect(db_path)
            df_sql = df.rename(columns=column_mapping)
            df_sql = df_sql.replace({np.nan: None, np.inf: None, -np.inf: None})
            df_sql.to_sql('data', conn, index=False, if_exists='replace')
            conn.close()

            # Build column info for frontend (using original column names)
            columns_info = []
            for col in df.columns:
                col_data = df[col]
                typ = ('numeric' if col in numeric_cols else
                       'datetime' if col in datetime_cols else 'categorical')
                sample = [convert_to_serializable(v) for v in col_data.dropna().head(3).tolist()]
                info = {
                    'name': col,
                    'type': typ,
                    'unique': int(col_data.nunique()) if not pd.isna(col_data.nunique()) else 0,
                    'nulls': int(col_data.isna().sum()),
                    'sample': sample
                }
                if typ == 'numeric':
                    try:
                        info.update({
                            'min': convert_to_serializable(col_data.min()),
                            'max': convert_to_serializable(col_data.max()),
                            'mean': convert_to_serializable(col_data.mean())
                        })
                    except:
                        pass
                columns_info.append(info)

            # Preview (first 20 rows)
            preview = []
            for _, row in df.head(20).iterrows():
                preview.append({col: convert_to_serializable(row[col]) for col in df.columns})

            # Store in session
            with data_lock:
                uploaded_data[session_id] = {
                    'filename': filename,
                    'db_path': db_path,
                    'column_mapping': column_mapping,
                    'reverse_mapping': reverse_mapping,
                    'total_rows': display_rows,
                    'file_total_rows': total_file_rows,
                    'total_cols': len(df.columns),
                    'original_columns': list(df.columns),
                    'numeric_columns': numeric_cols,
                    'categorical_columns': categorical_cols,
                    'datetime_columns': datetime_cols,
                    'converted_columns': converted_cols
                }

            msg = f'✅ Uploaded {display_rows} rows'
            if total_file_rows > display_rows:
                msg += f' (showing first {display_rows} of {total_file_rows})'
            if converted_cols:
                msg += f'. Converted {len(converted_cols)} columns to numeric.'

            return jsonify({
                'success': True,
                'message': msg,
                'filename': filename,
                'preview': preview,
                'columns': columns_info,
                'total_rows': display_rows,
                'file_total_rows': total_file_rows,
                'total_cols': len(df.columns),
                'numeric_columns': numeric_cols,
                'categorical_columns': categorical_cols,
                'datetime_columns': datetime_cols,
                'converted_columns': converted_cols
            })

        except Exception as e:
            logger.error(traceback.format_exc())
            return jsonify({'error': str(e)}), 400
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    except Exception as e:
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/ask_with_sql', methods=['POST'])
def ask_with_sql():
    """Convert natural language to SQL (using LLM if possible), execute, return results."""
    try:
        session_id = session.get('session_id')
        if not session_id or session_id not in uploaded_data:
            return jsonify({'error': 'Please upload a file first.'}), 400

        data = request.json
        question = data.get('question', '').strip()
        if not question:
            return jsonify({'error': 'No question provided'}), 400

        with data_lock:
            sd = uploaded_data[session_id]
            db_path = sd['db_path']
            reverse_mapping = sd['reverse_mapping']
            original_columns = sd['original_columns']
            numeric_cols = sd.get('numeric_columns', [])
            datetime_cols = sd.get('datetime_columns', [])
            # Build a simple schema for the LLM
            schema_lines = ["Table 'data' has columns:"]
            for col in original_columns:
                if col in numeric_cols:
                    schema_lines.append(f"- {col} (numeric)")
                elif col in datetime_cols:
                    schema_lines.append(f"- {col} (datetime)")
                else:
                    schema_lines.append(f"- {col} (categorical)")
            table_schema = "\n".join(schema_lines)

        sql_query = None
        rows = []
        columns = []

        # 1. Try to use the LLM for SQL generation
        if llm_module:
            try:
                sql_query = llm_module.generate_sql_query(question, table_schema)
                # Clean markdown fences
                if sql_query.startswith('```sql'):
                    sql_query = sql_query[6:]
                elif sql_query.startswith('```'):
                    sql_query = sql_query[3:]
                if sql_query.endswith('```'):
                    sql_query = sql_query[:-3]
                sql_query = sql_query.strip()
                logger.info(f"LLM generated SQL: {sql_query}")
            except Exception as e:
                logger.error(f"LLM SQL generation failed: {e}")
                sql_query = None

        # 2. Fallback: rule‑based patterns if LLM failed or not available
        if not sql_query:
            ql = question.lower()
            # --- Date range: last N days ---
            match = re.search(r'last\s+(\d+)\s+days?', ql)
            if match and datetime_cols:
                days = match.group(1)
                # Use the first datetime column found
                date_col = datetime_cols[0]
                sql_col = sd['column_mapping'][date_col]
                sql_query = f"SELECT * FROM data WHERE {sql_col} >= date('now', '-{days} days')"
                logger.info(f"Date rule matched: {sql_query}")
            # --- Other patterns (first, count, average, max, min, distribution) ---
            elif 'first' in ql or 'top' in ql:
                limit = 10 if '10' in ql else 5
                sql_query = f"SELECT * FROM data LIMIT {limit}"
            elif 'count' in ql or 'how many' in ql:
                sql_query = "SELECT COUNT(*) as count FROM data"
            elif 'average' in ql or 'mean' in ql:
                # pick first numeric column if none specified
                target = None
                for col in numeric_cols:
                    if col.lower() in ql:
                        target = col
                        break
                if not target and numeric_cols:
                    target = numeric_cols[0]
                if target:
                    sql_col = sd['column_mapping'][target]
                    sql_query = f"SELECT AVG(CAST({sql_col} AS FLOAT)) as average FROM data"
                else:
                    sql_query = "SELECT * FROM data LIMIT 5"
            elif 'maximum' in ql or 'max' in ql:
                target = None
                for col in numeric_cols:
                    if col.lower() in ql:
                        target = col
                        break
                if not target and numeric_cols:
                    target = numeric_cols[0]
                if target:
                    sql_col = sd['column_mapping'][target]
                    sql_query = f"SELECT MAX(CAST({sql_col} AS FLOAT)) as maximum FROM data"
                else:
                    sql_query = "SELECT * FROM data LIMIT 5"
            elif 'minimum' in ql or 'min' in ql:
                target = None
                for col in numeric_cols:
                    if col.lower() in ql:
                        target = col
                        break
                if not target and numeric_cols:
                    target = numeric_cols[0]
                if target:
                    sql_col = sd['column_mapping'][target]
                    sql_query = f"SELECT MIN(CAST({sql_col} AS FLOAT)) as minimum FROM data"
                else:
                    sql_query = "SELECT * FROM data LIMIT 5"
            elif 'distribution' in ql:
                # pick first categorical column that appears in question
                target = None
                for col in original_columns:
                    if col.lower() in ql and col not in numeric_cols:
                        target = col
                        break
                if not target and categorical_cols:
                    target = categorical_cols[0]
                if target:
                    sql_col = sd['column_mapping'][target]
                    sql_query = f"SELECT {sql_col}, COUNT(*) as count FROM data GROUP BY {sql_col} ORDER BY count DESC LIMIT 20"
                else:
                    sql_query = "SELECT * FROM data LIMIT 5"
            elif 'column' in ql:
                # return column list (handled separately)
                col_list = '\n'.join([f'• {c}' for c in original_columns])
                return jsonify({
                    'success': True,
                    'response': f"📋 **Columns ({len(original_columns)}):**\n{col_list}",
                    'sql_query': '-- column list',
                    'columns': ['Columns'],
                    'rows': [{'Columns': c} for c in original_columns],
                    'row_count': len(original_columns)
                })
            else:
                sql_query = "SELECT * FROM data LIMIT 5"

        # 3. Execute the SQL
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(sql_query)
            rows = cur.fetchall()
            col_names = [desc[0] for desc in cur.description]
            conn.close()

            # Map SQL column names back to original
            display_cols = []
            for c in col_names:
                if c in reverse_mapping:
                    display_cols.append(reverse_mapping[c])
                else:
                    display_cols.append(c)

            # Format rows
            formatted = []
            for r in rows:
                d = {}
                for i, orig in enumerate(col_names):
                    d[display_cols[i]] = convert_to_serializable(r[i])
                formatted.append(d)

            row_count = len(formatted)

            # Build response message
            if 'count' in sql_query.lower() and formatted:
                val = list(formatted[0].values())[0]
                response = f"📊 Total rows: **{val}**"
            elif 'average' in sql_query.lower() and formatted:
                val = list(formatted[0].values())[0]
                response = f"📈 Average: **{val:.2f}**" if val is not None else "No data"
            elif 'maximum' in sql_query.lower() and formatted:
                val = list(formatted[0].values())[0]
                response = f"📈 Maximum: **{val:.2f}**" if val is not None else "No data"
            elif 'minimum' in sql_query.lower() and formatted:
                val = list(formatted[0].values())[0]
                response = f"📉 Minimum: **{val:.2f}**" if val is not None else "No data"
            else:
                response = f"✅ Found **{row_count}** results"

            # Store conversation
            conv = {
                'question': question,
                'response': response,
                'sql': sql_query,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'row_count': row_count
            }
            if session_id not in conversations:
                conversations[session_id] = []
            conversations[session_id].append(conv)
            if len(conversations[session_id]) > 20:
                conversations[session_id] = conversations[session_id][-20:]

            return jsonify({
                'success': True,
                'response': response,
                'sql_query': sql_query,
                'columns': display_cols,
                'rows': formatted[:100],
                'row_count': row_count
            })

        except Exception as e:
            logger.error(f"SQL execution error: {e}")
            return jsonify({'error': f'SQL Error: {str(e)}', 'sql_query': sql_query}), 400

    except Exception as e:
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/get_chart', methods=['POST'])
def get_chart():
    """Generate a chart (bar/pie/line) based on selected columns."""
    try:
        session_id = session.get('session_id')
        if not session_id or session_id not in uploaded_data:
            return jsonify({'error': 'Upload a file first'}), 400

        req = request.json
        chart_type = req.get('chart_type')
        x_col = req.get('x_column')
        y_col = req.get('y_column')

        with data_lock:
            sd = uploaded_data[session_id]
            db_path = sd['db_path']
            rev = sd['reverse_mapping']
            num_cols = sd.get('numeric_columns', [])
            cat_cols = sd.get('categorical_columns', [])
            dt_cols = sd.get('datetime_columns', [])

        if not num_cols:
            return jsonify({'error': 'No numeric columns to chart'}), 400

        # Build query based on chart type
        if chart_type == 'pie':
            if not x_col or x_col not in cat_cols + dt_cols:
                return jsonify({'error': 'Pie chart needs a categorical/datetime column'}), 400
            sql_col = sd['column_mapping'][x_col]
            query = f"SELECT {sql_col}, COUNT(*) as cnt FROM data GROUP BY {sql_col} ORDER BY cnt DESC LIMIT 10"
        elif chart_type == 'bar':
            if not x_col or not y_col or y_col not in num_cols:
                return jsonify({'error': 'Bar chart needs a categorical X and numeric Y'}), 400
            x_sql = sd['column_mapping'][x_col]
            y_sql = sd['column_mapping'][y_col]
            query = f"SELECT {x_sql}, AVG(CAST({y_sql} AS FLOAT)) as val FROM data GROUP BY {x_sql} ORDER BY val DESC LIMIT 15"
        elif chart_type == 'line':
            if not y_col or y_col not in num_cols:
                return jsonify({'error': 'Line chart needs a numeric Y column'}), 400
            y_sql = sd['column_mapping'][y_col]
            query = f"SELECT {y_sql} FROM data WHERE {y_sql} IS NOT NULL ORDER BY ROWID LIMIT 50"
        else:
            return jsonify({'error': 'Invalid chart type'}), 400

        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            return jsonify({'error': 'No data for chart'}), 400

        plt.clf()
        fig, ax = plt.subplots(figsize=(10, 6))

        if chart_type == 'pie':
            labels = df.iloc[:, 0].astype(str).tolist()
            values = df.iloc[:, 1].tolist()
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFE194',
                      '#E6B89C', '#FE938C', '#9C89B8']
            ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors[:len(labels)])
            ax.set_title(f'Distribution of {x_col}')

        elif chart_type == 'bar':
            x_vals = df.iloc[:, 0].astype(str).tolist()
            y_vals = df.iloc[:, 1].tolist()
            bars = ax.bar(range(len(x_vals)), y_vals, color='#4ECDC4')
            ax.set_xticks(range(len(x_vals)))
            ax.set_xticklabels(x_vals, rotation=45, ha='right')
            ax.set_title(f'Average {y_col} by {x_col}')
            ax.set_ylabel(f'Avg {y_col}')
            for bar, val in zip(bars, y_vals):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                        f'{val:.2f}', ha='center', va='bottom')

        else:  # line
            y_vals = df.iloc[:, 0].tolist()
            ax.plot(range(len(y_vals)), y_vals, marker='o', color='#FF6B6B')
            ax.set_title(f'{y_col} Trend')
            ax.set_xlabel('Data point')
            ax.set_ylabel(y_col)
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=100)
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        return jsonify({'success': True, 'image': plot_url})

    except Exception as e:
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/conversation_history', methods=['GET'])
def conversation_history():
    session_id = session.get('session_id')
    if session_id and session_id in conversations:
        return jsonify({'success': True, 'conversations': conversations[session_id]})
    return jsonify({'success': True, 'conversations': []})

@app.route('/clear_data', methods=['POST'])
def clear_data():
    try:
        session_id = session.get('session_id')
        if session_id:
            with data_lock:
                if session_id in uploaded_data:
                    db_path = uploaded_data[session_id].get('db_path')
                    if db_path and os.path.exists(db_path):
                        os.remove(db_path)
                    del uploaded_data[session_id]
                if session_id in conversations:
                    del conversations[session_id]
        return jsonify({'success': True, 'message': 'Data cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ----------------------------------------------------------------------
# Error handlers
# ----------------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large (max 50MB)'}), 413

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# ----------------------------------------------------------------------
# Run
# ----------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)