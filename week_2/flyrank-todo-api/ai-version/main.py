"""
Tasks REST API
Python + FastAPI, in-memory storage (no database).

Run:
    pip install fastapi uvicorn
    uvicorn main:app --reload

Swagger UI:
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, field_validator
from typing import Optional, List

app = FastAPI(
    title="Tasks API",
    description="A simple in-memory task manager built with FastAPI.",
    version="1.0.0",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Turn FastAPI's default 422 validation errors into 400 Bad Request,
    matching the spec (e.g. missing/empty title on POST or PUT)."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

# ---------------------------------------------------------------------------
# In-memory storage
# ---------------------------------------------------------------------------
tasks: List[dict] = []
next_id: int = 1


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class TaskCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if v is None or not v.strip():
            raise ValueError("title must exist and cannot be empty")
        return v


class TaskUpdate(BaseModel):
    title: str
    done: Optional[bool] = False

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if v is None or not v.strip():
            raise ValueError("title must exist and cannot be empty")
        return v


class Task(BaseModel):
    id: int
    title: str
    done: bool


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def find_task(task_id: int) -> Optional[dict]:
    return next((t for t in tasks if t["id"] == task_id), None)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    """Basic info about the API."""
    return {"message": "Tasks API is running", "docs": "/docs"}


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Confirms the API is running."""
    return {"status": "ok"}


@app.get("/tasks", response_model=List[Task], status_code=status.HTTP_200_OK)
def list_tasks():
    """List every task."""
    return tasks


@app.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def get_task(task_id: int):
    """Return a specific task by id."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    """Add a new task. Body: {"title": "Buy milk"}"""
    global next_id
    new_task = {"id": next_id, "title": payload.title, "done": False}
    tasks.append(new_task)
    next_id += 1
    return new_task


@app.put("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_task(task_id: int, payload: TaskUpdate):
    """Update a task. Body: {"title": "Buy bread", "done": true}"""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    task["title"] = payload.title
    task["done"] = payload.done if payload.done is not None else task["done"]
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """Remove a task."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    tasks.remove(task)
    return None
