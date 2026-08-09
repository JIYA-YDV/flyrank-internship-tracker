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


# app/routes.py — route order matters

@router.get("/tasks", response_model=list[TaskResponse])
def get_all_tasks(
    search: Optional[str] = Query(default=None),
    done: Optional[bool] = Query(default=None),
    sort_alpha: bool = Query(default=False),
):
    return db_get_all_tasks(search=search, done=done, sort_alpha=sort_alpha)


# ⬇️ MUST come BEFORE /tasks/{task_id}
@router.get("/tasks/stats", response_model=StatsResponse)
def get_stats():
    return db_get_stats()


# ⬇️ Dynamic route comes AFTER all specific routes
@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = db_get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(body: TaskCreate):
    return db_create_task(title=body.title, done=body.done)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, body: TaskUpdate):
    task = db_update_task(task_id=task_id, title=body.title, done=body.done)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    deleted = db_delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task {task_id} deleted successfully"}
    return {"message": f"Task {task_id} deleted successfully"}