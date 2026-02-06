from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)  # Changed from UUID to string to match auth system


class Task(TaskBase, table=True):
    __tablename__ = "tasks"  # Explicitly define table name

    id: Optional[int] = Field(default=None, primary_key=True)  # Changed from UUID to int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None