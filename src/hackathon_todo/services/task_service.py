"""
Task service layer for business logic operations.

This module implements the business logic for task management,
coordinating between the domain models and storage layer.
"""

from __future__ import annotations

from typing import List, Optional

from ..domain.exceptions import NotFoundError, ValidationError
from ..domain.models import Task
from ..storage.interface import TaskStorage


class TaskService:
    """Service layer for task management operations."""

    def __init__(self, storage: TaskStorage) -> None:
        """
        Initialize the task service with a storage implementation.

        Args:
            storage: The storage implementation to use
        """
        self.storage = storage

    def add_task(self, title: str, description: str = "", completed: bool = False) -> Task:
        """
        Add a new task with validation.

        Args:
            title: The title of the task (1-200 characters)
            description: Optional description of the task (max 1000 characters)
            completed: Optional completion status (defaults to False)

        Returns:
            The created task

        Raises:
            ValidationError: If title or description validation fails
        """
        try:
            # Create a new task, which will validate the inputs
            task = Task(title=title, description=description, completed=completed)
        except Exception as e:
            # Convert Pydantic validation errors to our custom ValidationError
            from ..domain.exceptions import ValidationError as DomainValidationError
            raise DomainValidationError(str(e)) from e

        # Save the task to storage
        return self.storage.save_task(task)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all tasks
        """
        return self.storage.get_all_tasks()

    def get_task_by_id(self, task_id: str) -> Task:
        """
        Retrieve a specific task by its ID.

        Args:
            task_id: The unique identifier of the task

        Returns:
            The task if found

        Raises:
            NotFoundError: If the task doesn't exist
        """
        task = self.storage.get_task_by_id(task_id)
        if task is None:
            raise NotFoundError(f"Task with ID '{task_id}' does not exist")
        return task

    def update_task(self, task_id: str, title: Optional[str] = None, description: Optional[str] = None) -> Task:
        """
        Update an existing task.

        Args:
            task_id: The unique identifier of the task to update
            title: Optional new title for the task
            description: Optional new description for the task

        Returns:
            The updated task

        Raises:
            NotFoundError: If the task doesn't exist
            ValidationError: If new values fail validation
        """
        # Get the existing task
        existing_task = self.storage.get_task_by_id(task_id)
        if existing_task is None:
            raise NotFoundError(f"Task with ID '{task_id}' does not exist")

        # Prepare updates
        updates = {}
        if title is not None:
            try:
                # Validate the new title by creating a temporary task
                temp_task = Task(title=title, description=existing_task.description)
                updates['title'] = temp_task.title
            except Exception as e:
                from ..domain.exceptions import ValidationError as DomainValidationError
                raise DomainValidationError(str(e)) from e

        if description is not None:
            try:
                # Validate the new description by creating a temporary task
                temp_task = Task(title=existing_task.title, description=description)
                updates['description'] = temp_task.description
            except Exception as e:
                from ..domain.exceptions import ValidationError as DomainValidationError
                raise DomainValidationError(str(e)) from e

        # Perform the update
        updated_task = self.storage.update_task(task_id, **updates)
        if updated_task is None:
            raise NotFoundError(f"Task with ID '{task_id}' could not be updated")

        return updated_task

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.

        Args:
            task_id: The unique identifier of the task to delete

        Returns:
            True if the task was deleted, False if not found

        Raises:
            NotFoundError: If the task doesn't exist
        """
        success = self.storage.delete_task(task_id)
        if not success:
            raise NotFoundError(f"Task with ID '{task_id}' does not exist")
        return success

    def mark_complete(self, task_id: str) -> Task:
        """
        Mark a task as complete.

        Args:
            task_id: The unique identifier of the task to mark complete

        Returns:
            The updated task

        Raises:
            NotFoundError: If the task doesn't exist
        """
        task = self.storage.get_task_by_id(task_id)
        if task is None:
            raise NotFoundError(f"Task with ID '{task_id}' does not exist")

        # Update the task's completion status
        updated_task = self.storage.update_task(task_id, completed=True)
        if updated_task is None:
            raise NotFoundError(f"Task with ID '{task_id}' could not be updated")

        return updated_task

    def mark_incomplete(self, task_id: str) -> Task:
        """
        Mark a task as incomplete.

        Args:
            task_id: The unique identifier of the task to mark incomplete

        Returns:
            The updated task

        Raises:
            NotFoundError: If the task doesn't exist
        """
        task = self.storage.get_task_by_id(task_id)
        if task is None:
            raise NotFoundError(f"Task with ID '{task_id}' does not exist")

        # Update the task's completion status
        updated_task = self.storage.update_task(task_id, completed=False)
        if updated_task is None:
            raise NotFoundError(f"Task with ID '{task_id}' could not be updated")

        return updated_task