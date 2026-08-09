import sqlite3
from typing import Optional
from database import get_connection


def row_to_dict(row: sqlite3.Row) -> dict:
    """
    Converts a sqlite3.Row into a plain Python dictionary.
    Also converts done from integer (0/1) to a real boolean.
    """
    data = dict(row)
    data["done"] = bool(data["done"])
    return data


# ─────────────────────────────────────────
# READ
# ─────────────────────────────────────────

def db_get_all_tasks(
    search: Optional[str] = None,
    done: Optional[bool] = None,
    sort_alpha: bool = False
) -> list:
    """
    Returns all tasks from the database.
    Supports optional search, filter, and sort.
    """
    query = "SELECT id, title, done, created_at, updated_at FROM tasks WHERE 1=1"
    params = []

    if search is not None:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")

    if done is not None:
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
    Returns a single task by its id.
    Returns None if the task does not exist.
    """
    query = "SELECT id, title, done, created_at, updated_at FROM tasks WHERE id = ?"

    with get_connection() as conn:
        cursor = conn.execute(query, (task_id,))
        row = cursor.fetchone()

    if row is None:
        return None

    return row_to_dict(row)


# ─────────────────────────────────────────
# CREATE
# ─────────────────────────────────────────

def db_create_task(title: str, done: bool = False) -> dict:
    """
    Inserts a new task into the database.
    Returns the full created task including auto-generated id.
    """
    insert_sql = "INSERT INTO tasks (title, done) VALUES (?, ?)"
    select_sql = "SELECT id, title, done, created_at, updated_at FROM tasks WHERE id = ?"

    with get_connection() as conn:
        cursor = conn.execute(insert_sql, (title, 1 if done else 0))
        conn.commit()
        new_id = cursor.lastrowid
        row = conn.execute(select_sql, (new_id,)).fetchone()

    return row_to_dict(row)


# ─────────────────────────────────────────
# UPDATE
# ─────────────────────────────────────────

def db_update_task(
    task_id: int,
    title: Optional[str],
    done: Optional[bool]
) -> Optional[dict]:
    """
    Updates title and/or done for an existing task.
    Returns the updated task, or None if not found.
    """
    existing = db_get_task_by_id(task_id)
    if existing is None:
        return None

    final_title = title if title is not None else existing["title"]
    final_done = done if done is not None else existing["done"]

    update_sql = """
        UPDATE tasks
        SET title = ?,
            done = ?,
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
# DELETE
# ─────────────────────────────────────────

def db_delete_task(task_id: int) -> bool:
    """
    Deletes a task by id.
    Returns True if deleted, False if task was not found.
    """
    delete_sql = "DELETE FROM tasks WHERE id = ?"

    with get_connection() as conn:
        cursor = conn.execute(delete_sql, (task_id,))
        conn.commit()
        return cursor.rowcount > 0


# ─────────────────────────────────────────
# STATS
# ─────────────────────────────────────────

def db_get_stats() -> dict:
    """
    Returns total, completed, and pending task counts.
    Uses SQL COUNT() instead of counting in Python.
    """
    sql = """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN done = 1 THEN 1 ELSE 0 END) AS completed
        FROM tasks
    """

    with get_connection() as conn:
        row = conn.execute(sql).fetchone()

    total = row["total"] or 0
    completed = row["completed"] or 0

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": total - completed,
    }