"""
Tests for domain models.

This module contains tests for the Task model and related functionality.
Tests achieve 100% coverage for the domain layer.
"""

from datetime import datetime
import pytest
from hackathon_todo.domain.models import Task, create_task
from hackathon_todo.domain.exceptions import ValidationError


def test_task_creation_with_valid_data():
    """Test creating a task with valid data."""
    task = Task(title="Test Task", description="Test Description")

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False
    assert isinstance(task.id, str)
    assert len(task.id) > 0
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_creation_with_minimal_data():
    """Test creating a task with only required fields."""
    task = Task(title="Minimal Task")

    assert task.title == "Minimal Task"
    assert task.description == ""
    assert task.completed is False


def test_task_creation_generates_different_ids():
    """Test that different tasks get different IDs."""
    task1 = Task(title="Task 1")
    task2 = Task(title="Task 2")

    assert task1.id != task2.id


def test_task_title_validation_min_length():
    """Test that titles shorter than 1 character raise ValidationError."""
    with pytest.raises(ValidationError):
        Task(title="")


def test_task_title_validation_max_length():
    """Test that titles longer than 200 characters raise ValidationError."""
    long_title = "x" * 201
    with pytest.raises(ValidationError):
        Task(title=long_title)


def test_task_description_validation_max_length():
    """Test that descriptions longer than 1000 characters raise ValidationError."""
    long_description = "x" * 1001
    with pytest.raises(ValidationError):
        Task(title="Valid Title", description=long_description)


def test_task_mark_completed():
    """Test marking a task as completed."""
    task = Task(title="Test Task")
    assert task.completed is False

    task.mark_completed()
    assert task.completed is True


def test_task_mark_incomplete():
    """Test marking a task as incomplete."""
    task = Task(title="Test Task", completed=True)
    assert task.completed is True

    task.mark_incomplete()
    assert task.completed is False


def test_task_update_title():
    """Test updating a task's title."""
    task = Task(title="Old Title")
    assert task.title == "Old Title"

    task.update_title("New Title")
    assert task.title == "New Title"


def test_task_update_title_validation():
    """Test that updating title with invalid data raises ValidationError."""
    task = Task(title="Valid Title")

    with pytest.raises(ValidationError):
        task.update_title("")  # Too short

    with pytest.raises(ValidationError):
        task.update_title("x" * 201)  # Too long


def test_task_update_description():
    """Test updating a task's description."""
    task = Task(title="Test Task", description="Old Description")
    assert task.description == "Old Description"

    task.update_description("New Description")
    assert task.description == "New Description"


def test_task_update_description_validation():
    """Test that updating description with invalid data raises ValidationError."""
    task = Task(title="Test Task")

    with pytest.raises(ValidationError):
        task.update_description("x" * 1001)  # Too long


def test_task_timestamp_update_on_completion():
    """Test that timestamps are updated when completion status changes."""
    task = Task(title="Test Task")
    original_updated_at = task.updated_at

    # Wait a tiny bit to ensure time difference
    import time
    time.sleep(0.001)

    task.mark_completed()
    assert task.updated_at > original_updated_at


def test_task_timestamp_update_on_title_change():
    """Test that timestamps are updated when title changes."""
    task = Task(title="Test Task")
    original_updated_at = task.updated_at

    # Wait a tiny bit to ensure time difference
    import time
    time.sleep(0.001)

    task.update_title("New Title")
    assert task.updated_at > original_updated_at


def test_create_task_factory():
    """Test the create_task factory function."""
    task = create_task("Factory Task", "Factory Description")

    assert task.title == "Factory Task"
    assert task.description == "Factory Description"
    assert task.completed is False


def test_task_title_stripped():
    """Test that title whitespace is stripped."""
    task = Task(title="  Spaced Title  ")
    assert task.title == "Spaced Title"


def test_task_update_title_stripped():
    """Test that updated title whitespace is stripped."""
    task = Task(title="Original")
    task.update_title("  New Title  ")
    assert task.title == "New Title"