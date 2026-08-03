from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional

from models import TaskCreate, TaskUpdate, TaskResponse, StatsResponse
from crud import (
    db_get_all_tasks,
    db_get_task_by_id,
    db_create_task,
    db_update_task,
    db_delete_task,
    db_get_stats,
)

router = APIRouter()


# ─────────────────────────────────────────
# GET /tasks
# Returns all tasks. Supports optional filters.
# ─────────────────────────────────────────

@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    search:     Optional[str]  = Query(None, description="Filter by title keyword"),
    done:       Optional[bool] = Query(None, description="Filter by completion status"),
    sort_alpha: bool           = Query(False, description="Sort tasks alphabetically"),
):
    """
    Returns every task in the database.

    Optional query parameters:
        ?search=keyword   — Returns tasks whose title contains keyword
        ?done=true/false  — Filters by done status
        ?sort_alpha=true  — Alphabetical order instead of insertion order
    
    Examples:
        GET /tasks
        GET /tasks?done=false
        GET /tasks?search=learn&sort_alpha=true
    """
    tasks = db_get_all_tasks(search=search, done=done, sort_alpha=sort_alpha)
    return tasks


# ─────────────────────────────────────────
# GET /tasks/{id}
# Returns one task by primary key.
# ─────────────────────────────────────────

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """
    Returns a single task by its id.

    Raises:
        404 — if no task with that id exists
    """
    task = db_get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


# ─────────────────────────────────────────
# POST /tasks
# Inserts a new task into the database.
# ─────────────────────────────────────────

@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(body: TaskCreate):
    """
    Creates a new task and returns the created record.

    Request body:
        { "title": "Buy groceries", "done": false }

    Raises:
        400 — if title is missing or blank (enforced by Pydantic)
    
    Returns:
        201 with the full task record including auto-generated id
    """
    new_task = db_create_task(title=body.title, done=body.done)
    return new_task


# ─────────────────────────────────────────
# PUT /tasks/{id}
# Updates title and/or done status.
# ─────────────────────────────────────────

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, body: TaskUpdate):
    """
    Updates an existing task. All fields are optional.

    Request body examples:
        { "done": true }                   — mark complete
        { "title": "Updated title" }       — rename only
        { "title": "New", "done": false }  — update both

    Raises:
        404 — if no task with that id exists
        400 — if title is provided but is an empty string
    """
    updated = db_update_task(task_id=task_id, title=body.title, done=body.done)

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated


# ─────────────────────────────────────────
# DELETE /tasks/{id}
# Removes a task permanently.
# ─────────────────────────────────────────

@router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int):
    """
    Deletes a task from the database.

    Raises:
        404 — if no task with that id exists

    Returns:
        200 with a confirmation message
    """
    deleted = db_delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {"message": f"Task {task_id} deleted successfully"}


# ─────────────────────────────────────────
# GET /stats
# Returns task count statistics via SQL COUNT()
# ─────────────────────────────────────────

@router.get("/stats", response_model=StatsResponse)
def get_stats():
    """
    Returns task count statistics calculated entirely in SQL.

    Response:
        {
            "total_tasks": 5,
            "completed_tasks": 2,
            "pending_tasks": 3
        }
    """
    return db_get_stats()