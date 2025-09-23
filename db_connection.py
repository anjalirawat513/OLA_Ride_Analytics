import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()  # load values from .env

def get_connection():
    """Return a live connection to SQL Server."""
    conn_str = (
        f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"Trusted_Connection={os.getenv('DB_TRUSTED_CONNECTION')};"
    )
    return pyodbc.connect(conn_str)
