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

    def seed_tasks() -> None:
    """
    Inserts three starter tasks ONLY when the table is empty.

    Why check COUNT(*)?
    If we inserted without checking, restarting the server
    would keep adding duplicates. COUNT(*) = 0 means the
    database is brand new and needs starter data.

    This ensures seeds run exactly once in the lifetime
    of the database file.
    """
    with get_connection() as conn:
        # Count how many rows already exist
        cursor = conn.execute("SELECT COUNT(*) AS total FROM tasks")
        row = cursor.fetchone()
        count = row["total"]

        # Only seed when the table is completely empty
        if count == 0:
            seed_data = [
                ("Learn SQL fundamentals",           0),
                ("Connect SQLite to a FastAPI server", 1),
                ("Build an AI feature with Claude",  0),
            ]
            conn.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                seed_data
            )
            conn.commit()
            print(f"🌱 Seeded {len(seed_data)} example tasks.")
        else:
            print(f"📦 Database already has {count} task(s). Skipping seed.")


def init_db() -> None:
    """
    Master initialization function called at application startup.
    
    Order matters:
        1. Create the table first
        2. Then seed — the table must exist before inserting rows
    """
    create_table()
    seed_tasks()