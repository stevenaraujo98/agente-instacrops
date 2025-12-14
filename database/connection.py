import sqlite3
import os

DB_NAME = "farm_data.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

def get_db_connection():
    """Establishes and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn
