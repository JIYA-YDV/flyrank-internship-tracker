# app/database.py
"""
Database connection module — Postgres version.

This file is the ONLY file that knows we switched from SQLite to Postgres.
Everything above this layer (crud.py, routes.py, models.py) is unchanged.
That is the architecture working correctly.
"""

import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

# Load variables from .env file into os.environ
# This must run before we try to read any environment variables
load_dotenv()


def get_connection():
    """
    Open and return a connection to the Postgres database.

    Reads DATABASE_URL from environment variables (loaded from .env).

    Uses RealDictCursor so that rows come back as Python dictionaries.
    This is the same behaviour as SQLite's row_factory = sqlite3.Row.
    The rest of the code accesses rows as row["column_name"] either way.

    Returns:
        psycopg2 connection object

    Raises:
        RuntimeError: if DATABASE_URL is not set
        Exception: if Postgres cannot be reached
    """
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set.\n"
            "Make sure .env file exists with DATABASE_URL defined.\n"
            "See .env.example for the format."
        )

    connection = psycopg2.connect(
        database_url,
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    return connection


def init_db():
    """
    Called once at app startup to verify the database connection.

    In the SQLite version, this function created the table.
    In the Postgres version, the table is created by sql/init.sql
    which runs automatically when the Postgres Docker container
    starts for the first time.

    This function just confirms the connection is working.
    If it cannot connect, the app refuses to start (fail fast).

    Raises:
        RuntimeError: if the database cannot be reached
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Simple query to verify the connection works
        cursor.execute("SELECT 1")

        # Also verify our table exists
        cursor.execute(
            "SELECT COUNT(*) as count FROM tasks"
        )
        result = cursor.fetchone()

        conn.close()
        print("✅ Postgres connection verified")
        print(f"✅ Tasks table found with {result['count']} rows")

    except Exception as error:
        raise RuntimeError(
            f"Cannot connect to Postgres database.\n"
            f"Error: {error}\n"
            f"Make sure Docker is running and docker compose up was used."
        )