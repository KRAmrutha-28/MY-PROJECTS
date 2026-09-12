import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path='database.db'):  # Make sure this line exists!
        self.db_path = db_path
        self.current_table = None
        self.init_database()
        self.create_sample_data()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        conn.close()
    
    def create_sample_data(self):
        """Create sample sales data for demonstration"""
        np.random.seed(42)
        
        dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
        regions = ['North', 'South', 'East', 'West']
        products = ['Electronics', 'Clothing', 'Food', 'Books', 'Sports']
        
        data = []
        for date in dates[:500]:  # Limit to 500 records for demo
            for region in regions:
                for product in np.random.choice(products, 2):
                    data.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'region': region,
                        'product_category': product,
                        'sales_amount': np.random.randint(100, 10000),
                        'quantity': np.random.randint(1, 50),
                        'customer_segment': np.random.choice(['Premium', 'Regular', 'New']),
                        'profit_margin': np.random.uniform(0.1, 0.4)
                    })
        
        df = pd.DataFrame(data)
        self.save_to_database(df, 'sales_data')
        self.current_table = 'sales_data'
        return df
    
    def save_to_database(self, df, table_name):
        conn = sqlite3.connect(self.db_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        self.current_table = table_name
    
    def load_csv(self, file_path):
        """Load CSV file into database"""
        df = pd.read_csv(file_path)
        table_name = os.path.splitext(os.path.basename(file_path))[0]
        self.save_to_database(df, table_name)
        return df
    
    def execute_query(self, query):
        """Execute SQL query and return results as DataFrame"""
        conn = sqlite3.connect(self.db_path)
        try:
            df = pd.read_sql_query(query, conn)
            return df
        except Exception as e:
            raise Exception(f"Query execution failed: {str(e)}")
        finally:
            conn.close()
    
    def get_table_info(self):
        """Get information about the current table"""
        if not self.current_table:
            return None
        
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(f"SELECT * FROM {self.current_table} LIMIT 5", conn)
        
        info = {
            'table_name': self.current_table,
            'columns': list(df.columns),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'sample_data': df.to_dict('records')
        }
        conn.close()
        return info