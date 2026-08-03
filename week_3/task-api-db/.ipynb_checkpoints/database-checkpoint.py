import sqlite3
import os

# Absolute path to tasks.db, placed next to this file.
# Using an absolute path means the database is found no matter
# which folder you run uvicorn from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "tasks.db")


def get_connection() -> sqlite3.Connection:
    """
    Opens and returns a connection to the SQLite database.

    row_factory = sqlite3.Row lets us access columns by name
    instead of by index number.

        row["title"]  -> works like a dictionary
        row[1]        -> also still works like a tuple
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table() -> None:
    """
    Creates the tasks table if it does not already exist.

    Columns:
        id         - Auto-incrementing integer primary key
        title      - Text description of the task (required)
        done       - 0 = pending, 1 = complete (SQLite has no BOOLEAN type)
        created_at - Timestamp set once when the row is inserted
        updated_at - Timestamp refreshed every time the row changes

    "CREATE TABLE IF NOT EXISTS" makes this safe to run on every
    startup. If the table already exists, SQLite does nothing.
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
    conn = get_connection()
    try:
        conn.execute(sql)
        conn.commit()
        print("Table 'tasks' is ready.")
    finally:
        conn.close()


def seed_tasks() -> None:
    """
    Inserts three starter tasks ONLY when the table is empty.

    Why check COUNT(*) first?
    Without the check, every server restart would insert three
    more duplicate rows. COUNT(*) = 0 means the database is
    brand new, so seed data is needed exactly once.
    """
    conn = get_connection()
    try:
        cursor = conn.execute("SELECT COUNT(*) AS total FROM tasks")
        count = cursor.fetchone()["total"]

        if count == 0:
            seed_data = [
                ("Learn SQL fundamentals", 0),
                ("Connect SQLite to a FastAPI server", 1),
                ("Build an AI feature with Claude", 0),
            ]
            conn.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                seed_data,
            )
            conn.commit()
            print(f"Seeded {len(seed_data)} example tasks.")
        else:
            print(f"Database already has {count} task(s). Skipping seed.")
    finally:
        conn.close()


def init_db() -> None:
    """
    Master startup function.

    Order matters:
        1. create_table() - the table must exist first
        2. seed_tasks()   - only then can we insert rows
    """
    create_table()
    seed_tasks()