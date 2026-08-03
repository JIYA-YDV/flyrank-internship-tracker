from fastapi import APIRouter, HTTPException, status

from models import TaskCreate, TaskUpdate, TaskResponse
from crud import (
    db_get_all_tasks,
    db_get_task_by_id,
    db_create_task,
    db_update_task,
    db_delete_task,
)

router = APIRouter()


@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    """Returns every task stored in the database."""
    return db_get_all_tasks()


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
    A missing or blank title is rejected with 400 by Pydantic.
    """
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