# app/crud.py
"""
Database query functions — Postgres version.

Function names and signatures are IDENTICAL to the SQLite version.
This is why routes.py does not need to change at all.
Only the SQL syntax inside each function is different.

SQLite → Postgres changes:
  ?  placeholder  →  %s placeholder
  lastrowid       →  RETURNING * clause
  LIKE            →  ILIKE (case-insensitive in Postgres)
  row_factory     →  RealDictCursor (both make rows into dicts)
"""

from app.database import get_connection


# ── READ ──────────────────────────────────────────────────────────────


def db_get_all_tasks(
    search: str = None,
    done: bool = None,
    sort_alpha: bool = False
):
    """
    Retrieve all tasks with optional filtering and sorting.

    Builds the SQL query dynamically based on which filters are provided.
    Uses ILIKE for case-insensitive search (Postgres feature).

    Args:
        search:     keyword to search in title (case-insensitive)
        done:       True for completed tasks, False for pending
        sort_alpha: True to sort A→Z by title

    Returns:
        list of task dicts (empty list if no tasks match)
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Start with base query
    query = "SELECT * FROM tasks"
    params = []
    conditions = []

    # Add search filter if provided
    if search:
        # ILIKE = case-insensitive LIKE in Postgres
        # %s is the Postgres placeholder (not ? like SQLite)
        conditions.append("title ILIKE %s")
        params.append(f"%{search}%")

    # Add done filter if provided
    if done is not None:
        conditions.append("done = %s")
        params.append(done)

    # Attach WHERE clause if we have any conditions
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Add sorting if requested
    if sort_alpha:
        query += " ORDER BY title ASC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    # Convert RealDictRow objects to plain Python dicts
    return [dict(row) for row in rows]


def db_get_task_by_id(task_id: int):
    """
    Retrieve one task by its primary key.

    Args:
        task_id: integer ID of the task

    Returns:
        task dict if found, None if not found
    """
    conn = get_connection()
    cursor = conn.cursor()

    # %s is the placeholder — psycopg2 handles escaping safely
    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)   # params must be a tuple — note the comma
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return dict(row)


# ── CREATE ────────────────────────────────────────────────────────────


def db_create_task(title: str, done: bool = False):
    """
    Insert a new task and return the complete created row.

    Uses RETURNING * — a Postgres feature that returns the full row
    after insert, including the auto-generated id and timestamps.
    This replaces SQLite's lastrowid + second SELECT approach.

    Args:
        title: task title text
        done:  completion status (default False)

    Returns:
        created task dict with all fields including id and timestamps
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, done)
        VALUES (%s, %s)
        RETURNING *
        """,
        (title, done)
    )

    # RETURNING * gives us the complete inserted row immediately
    created_row = cursor.fetchone()

    # Postgres requires explicit commit for data-changing operations
    conn.commit()
    conn.close()

    return dict(created_row)


# ── UPDATE ────────────────────────────────────────────────────────────


def db_update_task(task_id: int, title: str = None, done: bool = None):
    """
    Update a task. Only updates the fields that are provided.

    If neither title nor done is provided, returns the task unchanged.
    Uses RETURNING * to get the updated row without a second query.

    Args:
        task_id: which task to update
        title:   new title (None = do not change)
        done:    new status (None = do not change)

    Returns:
        updated task dict, or None if task_id does not exist
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Build SET clause dynamically based on what was provided
    fields = []
    params = []

    if title is not None:
        fields.append("title = %s")
        params.append(title)

    if done is not None:
        fields.append("done = %s")
        params.append(done)

    # If nothing to update, return current task as-is
    if not fields:
        cursor.execute(
            "SELECT * FROM tasks WHERE id = %s",
            (task_id,)
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    # Always update the updated_at timestamp
    fields.append("updated_at = NOW()")

    # task_id goes last — it is the WHERE parameter
    params.append(task_id)

    query = f"""
        UPDATE tasks
        SET {', '.join(fields)}
        WHERE id = %s
        RETURNING *
    """

    cursor.execute(query, params)
    updated_row = cursor.fetchone()

    conn.commit()
    conn.close()

    if updated_row is None:
        return None

    return dict(updated_row)


# ── DELETE ────────────────────────────────────────────────────────────


def db_delete_task(task_id: int):
    """
    Delete a task by its ID.

    Args:
        task_id: which task to delete

    Returns:
        True if the task was found and deleted
        False if no task with that ID existed
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    # rowcount tells us how many rows were affected
    # 0 means the task did not exist
    # 1 means it was deleted
    deleted_count = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted_count > 0


# ── STATS ─────────────────────────────────────────────────────────────


def db_get_stats():
    """
    Return aggregate statistics about all tasks.

    Uses SQL aggregation — no Python counting loops needed.
    CASE WHEN done THEN 1 ELSE 0 END is standard SQL that works
    in both SQLite and Postgres.

    Returns:
        dict with keys: total, completed, pending
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*)                                    AS total,
            SUM(CASE WHEN done = true  THEN 1 ELSE 0 END) AS completed,
            SUM(CASE WHEN done = false THEN 1 ELSE 0 END) AS pending
        FROM tasks
        """
    )

    row = cursor.fetchone()
    conn.close()

    return dict(row)