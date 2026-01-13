"""
Task model definition with validation logic.

This module contains the Task dataclass with all validation rules
as specified in the project requirements.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Task(BaseModel):
    """
    Represents a todo task with validation rules.

    Attributes:
        id: Unique identifier for the task
        title: Task title (1-200 characters)
        description: Optional task description (max 1000 characters)
        completed: Boolean indicating completion status
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __init__(self, **data):
        """
        Initialize the Task with validation.

        This overrides the default __init__ to convert Pydantic validation errors
        to custom ValidationError exceptions.
        """
        try:
            super().__init__(**data)
        except Exception as e:
            # Check if this is a validation error from Pydantic
            if "validation" in str(e).lower() or "'ValidationError'" in str(type(e)):
                from .exceptions import ValidationError
                raise ValidationError(str(e)) from e
            else:
                raise

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """
        Validate the title length.

        Args:
            v: The title string to validate

        Returns:
            The validated title string

        Raises:
            ValidationError: If title length is not between 1 and 200 characters
        """
        if not (1 <= len(v) <= 200):
            from .exceptions import ValidationError
            raise ValidationError(f"Title must be between 1 and 200 characters, got {len(v)}")
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str) -> str:
        """
        Validate the description length.

        Args:
            v: The description string to validate

        Returns:
            The validated description string

        Raises:
            ValidationError: If description length exceeds 1000 characters
        """
        if len(v) > 1000:
            from .exceptions import ValidationError
            raise ValidationError(f"Description must not exceed 1000 characters, got {len(v)}")
        return v

    def mark_completed(self) -> None:
        """Mark the task as completed and update the timestamp."""
        self.completed = True
        self.update_timestamp()

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete and update the timestamp."""
        self.completed = False
        self.update_timestamp()

    def update_title(self, new_title: str) -> None:
        """
        Update the task title and timestamp.

        Args:
            new_title: The new title for the task
        """
        # This will trigger validation
        _ = self.validate_title(new_title)
        self.title = new_title.strip()
        self.update_timestamp()

    def update_description(self, new_description: str) -> None:
        """
        Update the task description and timestamp.

        Args:
            new_description: The new description for the task
        """
        # This will trigger validation
        _ = self.validate_description(new_description)
        self.description = new_description
        self.update_timestamp()

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp to current time."""
        self.updated_at = datetime.now()


def create_task(title: str, description: str = "") -> Task:
    """
    Factory function to create a new task with validation.

    Args:
        title: The title for the new task
        description: Optional description for the new task

    Returns:
        A new Task instance
    """
    try:
        # Pydantic will handle validation during instantiation
        return Task(title=title, description=description)
    except Exception as e:
        # Convert Pydantic validation errors to our custom ValidationError
        raise ValidationError(str(e)) from e