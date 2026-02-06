from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    title: str
    description: Optional[str] = None


class TaskRead(TaskBase):
    id: int  # Changed from uuid.UUID to int to match database
    user_id: str  # Changed from uuid.UUID to str to match auth system
    completed: bool
    created_at: datetime
    updated_at: datetime


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskToggleComplete(BaseModel):
    completed: bool