# app/models.py
"""
Pydantic models for request validation and response shaping.

Updated for Postgres:
  - created_at / updated_at are now `datetime` (Postgres returns real timestamps)
  - done is now a real `bool` (Postgres has a native BOOLEAN type)
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Validates the body of POST /tasks"""
    title: str = Field(..., min_length=1, description="Task title, cannot be empty")
    done: bool = Field(default=False, description="Completion status")


class TaskUpdate(BaseModel):
    """Validates the body of PUT /tasks/{id} — all fields optional"""
    title: Optional[str] = Field(default=None, min_length=1)
    done: Optional[bool] = Field(default=None)


class TaskResponse(BaseModel):
    """Shapes every task returned to the client"""
    id: int
    title: str
    done: bool
    created_at: datetime     # ← was str in the SQLite version
    updated_at: datetime     # ← was str in the SQLite version


class StatsResponse(BaseModel):
    """Shapes the GET /tasks/stats response"""
    total: int
    completed: int
    pending: int