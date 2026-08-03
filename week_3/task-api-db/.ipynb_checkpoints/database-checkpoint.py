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

    def create_table() -> None:
    """
    Creates the tasks table if it does not already exist.

    Schema:
        id        — Auto-incrementing integer primary key
        title     — Text description of the task (required)
        done      — 0 = not done, 1 = done (SQLite has no boolean type)
        created_at — Timestamp set automatically when row is inserted
        updated_at — Timestamp updated every time the row changes

    CREATE TABLE IF NOT EXISTS means this is safe to call
    every time the application starts. If the table already
    exists, SQLite simply does nothing.
    """
    sql = """
        CREATE TABLE IF NOT EXISTS tasks (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT    NOT NULL,
            done       INTEGER NOT NULL DEFAULT 0,
            created_at TEXT    DEFAULT (datetime('now')),
            updated_at TEXT    DEFAULT (datetime('now'))
        )
    """
    with get_connection() as conn:
        conn.execute(sql)
        conn.commit()
    print("✅ Table 'tasks' is ready.")