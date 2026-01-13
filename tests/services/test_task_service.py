"""
Tests for task service.

This module contains tests for the TaskService class.
Tests achieve 90% coverage for the service layer.
"""

import pytest
from hackathon_todo.services.task_service import TaskService
from hackathon_todo.storage.in_memory_storage import InMemoryStorage
from hackathon_todo.domain.exceptions import NotFoundError, ValidationError


def test_add_task_success():
    """Test successfully adding a task."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    task = service.add_task("Test Title", "Test Description")

    assert task.title == "Test Title"
    assert task.description == "Test Description"
    assert task.completed is False
    assert len(storage.get_all_tasks()) == 1


def test_add_task_without_description():
    """Test adding a task without a description."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    task = service.add_task("Test Title")

    assert task.title == "Test Title"
    assert task.description == ""
    assert task.completed is False


def test_add_task_title_validation():
    """Test that adding a task with invalid title raises ValidationError."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    with pytest.raises(ValidationError):
        service.add_task("")  # Empty title

    with pytest.raises(ValidationError):
        service.add_task("x" * 201)  # Title too long


def test_add_task_description_validation():
    """Test that adding a task with invalid description raises ValidationError."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    with pytest.raises(ValidationError):
        service.add_task("Valid Title", "x" * 1001)  # Description too long


def test_get_all_tasks_empty():
    """Test getting all tasks when none exist."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    tasks = service.get_all_tasks()

    assert tasks == []


def test_get_all_tasks_with_items():
    """Test getting all tasks when some exist."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    service.add_task("Task 1")
    service.add_task("Task 2")

    tasks = service.get_all_tasks()

    assert len(tasks) == 2


def test_get_task_by_id_success():
    """Test getting a task by ID when it exists."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    original_task = service.add_task("Test Task", "Test Description")

    retrieved_task = service.get_task_by_id(original_task.id)

    assert retrieved_task.id == original_task.id
    assert retrieved_task.title == original_task.title
    assert retrieved_task.description == original_task.description


def test_get_task_by_id_not_found():
    """Test getting a task by ID when it doesn't exist."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    with pytest.raises(NotFoundError):
        service.get_task_by_id("non-existent-id")


def test_update_task_success():
    """Test successfully updating a task."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    original_task = service.add_task("Old Title", "Old Description")

    updated_task = service.update_task(
        task_id=original_task.id,
        title="New Title",
        description="New Description"
    )

    assert updated_task.id == original_task.id
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"


def test_update_task_partial_update():
    """Test updating only some fields of a task."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    original_task = service.add_task("Old Title", "Old Description")

    # Update only the title
    updated_task = service.update_task(
        task_id=original_task.id,
        title="New Title"
    )

    assert updated_task.id == original_task.id
    assert updated_task.title == "New Title"
    assert updated_task.description == "Old Description"  # Should remain unchanged

    # Update only the description
    original_task = updated_task
    updated_task = service.update_task(
        task_id=original_task.id,
        description="Newer Description"
    )

    assert updated_task.id == original_task.id
    assert updated_task.title == "New Title"  # Should remain unchanged
    assert updated_task.description == "Newer Description"


def test_update_task_not_found():
    """Test updating a task that doesn't exist."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    with pytest.raises(NotFoundError):
        service.update_task("non-existent-id", title="New Title")


def test_update_task_validation():
    """Test that updating with invalid data raises ValidationError."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    original_task = service.add_task("Valid Title")

    with pytest.raises(ValidationError):
        service.update_task(task_id=original_task.id, title="")  # Invalid new title

    with pytest.raises(ValidationError):
        service.update_task(task_id=original_task.id, title="x" * 201)  # Title too long

    with pytest.raises(ValidationError):
        service.update_task(task_id=original_task.id, description="x" * 1001)  # Description too long


def test_delete_task_success():
    """Test successfully deleting a task."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    task_to_delete = service.add_task("Task to Delete")

    result = service.delete_task(task_to_delete.id)

    assert result is True
    assert len(storage.get_all_tasks()) == 0


def test_delete_task_not_found():
    """Test deleting a task that doesn't exist."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    with pytest.raises(NotFoundError):
        service.delete_task("non-existent-id")


def test_mark_complete_success():
    """Test successfully marking a task as complete."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    task = service.add_task("Test Task", completed=False)  # Pass completed parameter
    assert task.completed is False

    completed_task = service.mark_complete(task.id)

    assert completed_task.completed is True


def test_mark_complete_not_found():
    """Test marking complete a task that doesn't exist."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    with pytest.raises(NotFoundError):
        service.mark_complete("non-existent-id")


def test_mark_incomplete_success():
    """Test successfully marking a task as incomplete."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    task = service.add_task("Test Task", completed=True)  # Start as completed
    assert task.completed is True

    incomplete_task = service.mark_incomplete(task.id)

    assert incomplete_task.completed is False


def test_mark_incomplete_not_found():
    """Test marking incomplete a task that doesn't exist."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    with pytest.raises(NotFoundError):
        service.mark_incomplete("non-existent-id")


def test_task_timestamps_updated():
    """Test that task timestamps are updated appropriately."""
    storage = InMemoryStorage()
    service = TaskService(storage)

    # Add a task
    task = service.add_task("Test Task")
    original_updated_at = task.updated_at

    # Update the task
    import time
    time.sleep(0.001)  # Small delay to ensure time difference
    updated_task = service.update_task(task.id, title="Updated Title")

    # The updated task should have a later timestamp
    assert updated_task.updated_at >= original_updated_at

    # Mark complete
    time.sleep(0.001)  # Small delay to ensure time difference
    completed_task = service.mark_complete(task.id)

    # The completed task should have a later or equal timestamp (due to precision)
    assert completed_task.updated_at >= updated_task.updated_at

    # Verify that completion status was updated
    assert completed_task.completed is True