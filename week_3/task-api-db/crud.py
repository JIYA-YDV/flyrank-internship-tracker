import sqlite3
from typing import Optional
from database import get_connection


def row_to_dict(row: sqlite3.Row) -> dict:
    """
    Converts a sqlite3.Row object into a plain Python dict.
    
    sqlite3.Row behaves like a dict but is not one.
    Converting it makes it easy to pass to Pydantic models.
    
    Also converts the integer `done` value (0 or 1) to a
    proper Python boolean so Pydantic and JSON output are clean.
    """
    data = dict(row)
    data["done"] = bool(data["done"])
    return data


# ─────────────────────────────────────────
# READ QUERIES
# ─────────────────────────────────────────

def db_get_all_tasks(
    search: Optional[str] = None,
    done: Optional[bool] = None,
    sort_alpha: bool = False
) -> list[dict]:
    """
    Fetches all tasks with optional filtering and sorting.

    Parameters:
        search     — LIKE filter on title column
        done       — Filter by completion status
        sort_alpha — If True, sort results alphabetically by title

    SQL Pattern:
        We build the query dynamically by appending WHERE
        clauses and parameters only when filters are provided.
        This avoids writing separate queries for every combination.
    """
    query = "SELECT id, title, done, created_at, updated_at FROM tasks WHERE 1=1"
    params = []

    if search is not None:
        # LIKE '%value%' matches any title containing the search string
        query += " AND title LIKE ?"
        params.append(f"%{search}%")

    if done is not None:
        # Convert Python bool to SQLite integer (True=1, False=0)
        query += " AND done = ?"
        params.append(1 if done else 0)

    if sort_alpha:
        query += " ORDER BY title ASC"
    else:
        query += " ORDER BY id ASC"

    with get_connection() as conn:
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()

    return [row_to_dict(r) for r in rows]


def db_get_task_by_id(task_id: int) -> Optional[dict]:
    """
    Fetches a single task by its primary key.

    Returns:
        A dict if the task exists, or None if not found.
        The caller is responsible for raising 404.
    """
    query = "SELECT id, title, done, created_at, updated_at FROM tasks WHERE id = ?"

    with get_connection() as conn:
        cursor = conn.execute(query, (task_id,))
        row = cursor.fetchone()

    if row is None:
        return None

    return row_to_dict(row)


# ─────────────────────────────────────────
# CREATE QUERY
# ─────────────────────────────────────────

def db_create_task(title: str, done: bool = False) -> dict:
    """
    Inserts a new row into the tasks table.

    Steps:
        1. INSERT the new row
        2. Use lastrowid to get the auto-generated id
        3. SELECT that row back so we return the full record

    Why SELECT after INSERT?
        We need the auto-generated id and the default timestamps.
        They are set by SQLite, so we must read them back.
    """
    insert_sql = """
        INSERT INTO tasks (title, done)
        VALUES (?, ?)
    """
    select_sql = "SELECT id, title, done, created_at, updated_at FROM tasks WHERE id = ?"

    with get_connection() as conn:
        cursor = conn.execute(insert_sql, (title, 1 if done else 0))
        conn.commit()
        new_id = cursor.lastrowid

        row = conn.execute(select_sql, (new_id,)).fetchone()

    return row_to_dict(row)


# ─────────────────────────────────────────
# UPDATE QUERY
# ─────────────────────────────────────────

def db_update_task(task_id: int, title: Optional[str], done: Optional[bool]) -> Optional[dict]:
    """
    Updates one or both fields of an existing task.

    Strategy — merge with existing values:
        1. Fetch the current row
        2. Replace only the fields provided by the client
        3. Run UPDATE with the final merged values
        4. Return the updated row

    Also updates the updated_at timestamp so we track
    when the task was last modified.
    """
    existing = db_get_task_by_id(task_id)
    if existing is None:
        return None

    # Use new values if provided, otherwise keep existing values
    final_title = title if title is not None else existing["title"]
    final_done  = done  if done  is not None else existing["done"]

    update_sql = """
        UPDATE tasks
        SET title      = ?,
            done       = ?,
            updated_at = datetime('now')
        WHERE id = ?
    """
    select_sql = "SELECT id, title, done, created_at, updated_at FROM tasks WHERE id = ?"

    with get_connection() as conn:
        conn.execute(update_sql, (final_title, 1 if final_done else 0, task_id))
        conn.commit()
        row = conn.execute(select_sql, (task_id,)).fetchone()

    return row_to_dict(row)


# ─────────────────────────────────────────
# DELETE QUERY
# ─────────────────────────────────────────

def db_delete_task(task_id: int) -> bool:
    """
    Deletes a task by id.

    Returns:
        True  — task existed and was deleted
        False — task was not found (caller raises 404)

    rowcount tells us how many rows were affected.
    If 0 rows were deleted, the id did not exist.
    """
    delete_sql = "DELETE FROM tasks WHERE id = ?"

    with get_connection() as conn:
        cursor = conn.execute(delete_sql, (task_id,))
        conn.commit()
        return cursor.rowcount > 0


# ─────────────────────────────────────────
# STATS QUERY
# ─────────────────────────────────────────

def db_get_stats() -> dict:
    """
    Returns task counts calculated entirely in SQL using COUNT().
    
    Using SQL COUNT() is more efficient than fetching all rows
    and counting them in Python — the database does the math.
    """
    sql = """
        SELECT
            COUNT(*)              AS total,
            SUM(CASE WHEN done = 1 THEN 1 ELSE 0 END) AS completed
        FROM tasks
    """
    with get_connection() as conn:
        row = conn.execute(sql).fetchone()

    total     = row["total"]     or 0
    completed = row["completed"] or 0

    return {
        "total_tasks":     total,
        "completed_tasks": completed,
        "pending_tasks":   total - completed,
    }