"""
In-memory storage implementation for task operations.

This module provides an in-memory implementation of the TaskStorage interface
for development and testing purposes.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from ..domain.exceptions import StorageError
from ..domain.models import Task
from .interface import TaskStorage


class InMemoryStorage(TaskStorage):
    """In-memory implementation of TaskStorage interface."""

    def __init__(self) -> None:
        """Initialize the in-memory storage with an empty task dictionary."""
        self._tasks: Dict[str, Task] = {}

    def save_task(self, task: Task) -> Task:
        """
        Save a task to in-memory storage.

        Args:
            task: The task to save

        Returns:
            The saved task
        """
        try:
            self._tasks[task.id] = task
            return task
        except Exception as e:
            raise StorageError(f"Failed to save task: {str(e)}")

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from in-memory storage.

        Returns:
            List of all tasks in storage
        """
        try:
            return list(self._tasks.values())
        except Exception as e:
            raise StorageError(f"Failed to retrieve tasks: {str(e)}")

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a specific task by its ID.

        Args:
            task_id: The unique identifier of the task

        Returns:
            The task if found, None otherwise
        """
        try:
            return self._tasks.get(task_id)
        except Exception as e:
            raise StorageError(f"Failed to retrieve task {task_id}: {str(e)}")

    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """
        Update a task with the provided fields.

        Args:
            task_id: The unique identifier of the task to update
            **kwargs: Fields to update

        Returns:
            The updated task if found, None otherwise
        """
        try:
            task = self._tasks.get(task_id)
            if task is None:
                return None

            # Update the task fields
            for field, value in kwargs.items():
                if hasattr(task, field):
                    setattr(task, field, value)

            # Update the timestamp
            task.update_timestamp()

            # Save back to storage
            self._tasks[task_id] = task
            return task
        except Exception as e:
            raise StorageError(f"Failed to update task {task_id}: {str(e)}")

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task from in-memory storage.

        Args:
            task_id: The unique identifier of the task to delete

        Returns:
            True if the task was deleted, False if not found
        """
        try:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False
        except Exception as e:
            raise StorageError(f"Failed to delete task {task_id}: {str(e)}")