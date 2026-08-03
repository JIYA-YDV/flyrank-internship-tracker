import sqlite3
from typing import Optional

# Path to the SQLite database file
DB_FILE = "tasks.db"


def get_connection() -> sqlite3.Connection:
    """
    Opens and returns a connection to the SQLite database.
    
    row_factory = sqlite3.Row allows us to access columns
    by name like a dictionary instead of by index number.
    
    Example:
        row["title"]  ✅  works like a dict
        row[1]        ✅  also works like a tuple
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn