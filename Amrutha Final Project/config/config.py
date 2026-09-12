import os

import MySQLdb
import MySQLdb.cursors


def get_db_connect():
    return MySQLdb.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', ''),
        db=os.environ.get('DB_NAME', 'amrutha'),
        cursorclass=MySQLdb.cursors.DictCursor
    )
