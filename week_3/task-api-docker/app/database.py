# app/database.py
"""
Database connection module — Postgres version.

Includes retry logic for startup timing issues in Docker.
"""

import os
import time
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """
    Open and return a connection to the Postgres database.

    Reads DATABASE_URL from environment variables (loaded from .env).
    Uses RealDictCursor so rows come back as Python dictionaries.

    Returns:
        psycopg2 connection object

    Raises:
        RuntimeError: if DATABASE_URL is not set
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

    Retries up to 5 times with a 2-second wait between attempts.
    This handles the case where the app starts slightly before
    Postgres is fully ready to accept connections.

    Raises:
        RuntimeError: if all retry attempts fail
    """
    max_retries = 5
    wait_seconds = 2

    for attempt in range(1, max_retries + 1):
        try:
            print(f"⏳ Connecting to Postgres... (attempt {attempt}/{max_retries})")

            conn = get_connection()
            cursor = conn.cursor()

            # Verify connection works
            cursor.execute("SELECT 1")

            # Verify our table exists and count rows
            cursor.execute("SELECT COUNT(*) as count FROM tasks")
            result = cursor.fetchone()

            conn.close()

            print("✅ Postgres connection verified")
            print(f"✅ Tasks table found with {result['count']} rows")
            return  # success — exit the function

        except Exception as error:
            print(f"❌ Attempt {attempt} failed: {error}")

            if attempt < max_retries:
                print(f"⏳ Waiting {wait_seconds} seconds before retry...")
                time.sleep(wait_seconds)
            else:
                raise RuntimeError(
                    f"Cannot connect to Postgres after {max_retries} attempts.\n"
                    f"Last error: {error}\n"
                    f"Make sure docker compose up is running."
                )