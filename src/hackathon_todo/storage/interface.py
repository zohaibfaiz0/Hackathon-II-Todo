"""
Abstract interface for task storage operations.

This module defines the abstract base class for all storage implementations,
enabling dependency inversion as required by the architecture.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from ..domain.models import Task


class TaskStorage(ABC):
    """Abstract base class defining the interface for task storage operations."""

    @abstractmethod
    def save_task(self, task: Task) -> Task:
        """
        Save a task to storage.

        Args:
            task: The task to save

        Returns:
            The saved task with any storage-specific updates
        """
        pass

    @abstractmethod
    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from storage.

        Returns:
            List of all tasks in storage
        """
        pass

    @abstractmethod
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a specific task by its ID.

        Args:
            task_id: The unique identifier of the task

        Returns:
            The task if found, None otherwise
        """
        pass

    @abstractmethod
    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """
        Update a task with the provided fields.

        Args:
            task_id: The unique identifier of the task to update
            **kwargs: Fields to update

        Returns:
            The updated task if found, None otherwise
        """
        pass

    @abstractmethod
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task from storage.

        Args:
            task_id: The unique identifier of the task to delete

        Returns:
            True if the task was deleted, False if not found
        """
        pass