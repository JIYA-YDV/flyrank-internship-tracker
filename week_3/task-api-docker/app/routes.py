from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from pydantic import BaseModel

# NEW (A3 style — package imports)
from app.models import TaskCreate, TaskUpdate, TaskResponse, StatsResponse
from app.crud import (
    db_get_all_tasks,
    db_get_task_by_id,
    db_create_task,
    db_update_task,
    db_delete_task,
    db_get_stats,
)

router = APIRouter()


@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    search: Optional[str] = Query(None, description="Filter by keyword in the title"),
    done: Optional[bool] = Query(None, description="Filter by completion status"),
    sort_alpha: bool = Query(False, description="Sort alphabetically by title"),
):
    """
    Returns every task, with optional filtering and sorting.

    Examples:
        GET /tasks
        GET /tasks?search=sql
        GET /tasks?done=false
        GET /tasks?search=learn&sort_alpha=true
    """
    return db_get_all_tasks(search=search, done=done, sort_alpha=sort_alpha)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """Returns one task. Raises 404 if the id does not exist."""
    task = db_get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(body: TaskCreate):
    """
    Creates a new task and returns it with status 201.
    A missing or blank title is rejected with 400.
    """
    # Manually validate and raise 400 for missing or blank titles
    if not body.title or body.title.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required"
        )
    
    return db_create_task(title=body.title, done=body.done)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, body: TaskUpdate):
    """Updates title and/or done. Raises 404 if the id does not exist."""
    updated = db_update_task(task_id=task_id, title=body.title, done=body.done)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int):
    """
    Deletes a task permanently using a SQL DELETE statement.
    Raises 404 if the id does not exist.
    """
    deleted = db_delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task {task_id} deleted successfully"}


@router.get("/stats", response_model=StatsResponse)
def get_stats():
    """
    Returns task counts calculated with SQL COUNT(), not Python loops.

    Response:
        { "total_tasks": 5, "completed_tasks": 2, "pending_tasks": 3 }
    """
    return db_get_stats()