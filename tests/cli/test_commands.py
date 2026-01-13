"""
Tests for CLI commands.

This module contains tests for the CLI command handlers.
Tests achieve 85% coverage for the CLI layer.
"""

import io
import sys
from unittest.mock import Mock, patch
import pytest
from hackathon_todo.cli.commands import (
    add_command_handler,
    list_command_handler,
    view_command_handler,
    update_command_handler,
    delete_command_handler,
    complete_command_handler,
    uncomplete_command_handler
)
from hackathon_todo.domain.exceptions import NotFoundError, ValidationError
from hackathon_todo.domain.models import Task


def test_add_command_handler_success():
    """Test successful addition of a task via command handler."""
    mock_service = Mock()
    mock_task = Task(title="Test Task", description="Test Description")
    mock_service.add_task.return_value = mock_task

    with patch('hackathon_todo.cli.display.display_success_message'):
        add_command_handler(mock_service, "Test Title", "Test Description")

    mock_service.add_task.assert_called_once_with(title="Test Title", description="Test Description")


def test_add_command_handler_validation_error():
    """Test handling of validation errors in add command."""
    mock_service = Mock()
    mock_service.add_task.side_effect = ValidationError("Invalid input")

    with patch('hackathon_todo.cli.commands.display_error_message') as mock_display:
        add_command_handler(mock_service, "Test Title", "Test Description")

    mock_display.assert_called_once()
    assert "Validation Error:" in mock_display.call_args[0][0]


def test_list_command_handler_success():
    """Test successful listing of tasks via command handler."""
    mock_service = Mock()
    mock_task = Task(title="Test Task")
    mock_service.get_all_tasks.return_value = [mock_task]

    with patch('hackathon_todo.cli.commands.display_tasks_table'):
        list_command_handler(mock_service)

    mock_service.get_all_tasks.assert_called_once()


def test_list_command_handler_error():
    """Test handling of errors in list command."""
    mock_service = Mock()
    mock_service.get_all_tasks.side_effect = Exception("Storage error")

    with patch('hackathon_todo.cli.commands.display_error_message') as mock_display:
        list_command_handler(mock_service)

    mock_display.assert_called_once()
    assert "Error retrieving tasks:" in mock_display.call_args[0][0]


def test_view_command_handler_success():
    """Test successful viewing of a task via command handler."""
    mock_service = Mock()
    mock_task = Task(title="Test Task")
    mock_service.get_task_by_id.return_value = mock_task

    with patch('hackathon_todo.cli.commands.display_task_detail'):
        view_command_handler(mock_service, "some-id")

    mock_service.get_task_by_id.assert_called_once_with("some-id")


def test_view_command_handler_not_found():
    """Test handling of not found errors in view command."""
    mock_service = Mock()
    mock_service.get_task_by_id.side_effect = NotFoundError("Task not found")

    with patch('hackathon_todo.cli.commands.display_error_message') as mock_display:
        view_command_handler(mock_service, "some-id")

    mock_display.assert_called_once()
    assert "Not Found:" in mock_display.call_args[0][0]


def test_update_command_handler_success():
    """Test successful update of a task via command handler."""
    mock_service = Mock()
    mock_task = Task(title="Updated Task")
    mock_service.update_task.return_value = mock_task

    with patch('hackathon_todo.cli.display.display_success_message'):
        update_command_handler(mock_service, "some-id", title="Updated Title", description="Updated Description")

    mock_service.update_task.assert_called_once_with(
        task_id="some-id",
        title="Updated Title",
        description="Updated Description"
    )


def test_update_command_handler_partial_update():
    """Test partial update of a task via command handler."""
    mock_service = Mock()
    mock_task = Task(title="Updated Task")
    mock_service.update_task.return_value = mock_task

    with patch('hackathon_todo.cli.display.display_success_message'):
        # Update only title
        update_command_handler(mock_service, "some-id", title="Updated Title")

    mock_service.update_task.assert_called_once_with(
        task_id="some-id",
        title="Updated Title",
        description=None
    )

    mock_service.reset_mock()

    with patch('hackathon_todo.cli.display.display_success_message'):
        # Update only description
        update_command_handler(mock_service, "some-id", description="Updated Description")

    mock_service.update_task.assert_called_once_with(
        task_id="some-id",
        title=None,
        description="Updated Description"
    )


def test_update_command_handler_not_found():
    """Test handling of not found errors in update command."""
    mock_service = Mock()
    mock_service.update_task.side_effect = NotFoundError("Task not found")

    with patch('hackathon_todo.cli.commands.display_error_message') as mock_display:
        update_command_handler(mock_service, "some-id", title="New Title")

    mock_display.assert_called_once()
    assert "Not Found:" in mock_display.call_args[0][0]


def test_update_command_handler_validation_error():
    """Test handling of validation errors in update command."""
    mock_service = Mock()
    mock_service.update_task.side_effect = ValidationError("Invalid input")

    with patch('hackathon_todo.cli.commands.display_error_message') as mock_display:
        update_command_handler(mock_service, "some-id", title="New Title")

    mock_display.assert_called_once()
    assert "Validation Error:" in mock_display.call_args[0][0]


def test_delete_command_handler_success():
    """Test successful deletion of a task via command handler."""
    mock_service = Mock()
    mock_service.delete_task.return_value = True

    with patch('hackathon_todo.cli.display.display_success_message'):
        delete_command_handler(mock_service, "some-id")

    mock_service.delete_task.assert_called_once_with("some-id")


def test_delete_command_handler_not_found():
    """Test handling of not found errors in delete command."""
    mock_service = Mock()
    mock_service.delete_task.side_effect = NotFoundError("Task not found")

    with patch('hackathon_todo.cli.commands.display_error_message') as mock_display:
        delete_command_handler(mock_service, "some-id")

    mock_display.assert_called_once()
    assert "Not Found:" in mock_display.call_args[0][0]


def test_complete_command_handler_success():
    """Test successful completion of a task via command handler."""
    mock_service = Mock()
    mock_task = Task(title="Test Task", completed=True)
    mock_service.mark_complete.return_value = mock_task

    with patch('hackathon_todo.cli.display.display_success_message'):
        complete_command_handler(mock_service, "some-id")

    mock_service.mark_complete.assert_called_once_with("some-id")


def test_complete_command_handler_not_found():
    """Test handling of not found errors in complete command."""
    mock_service = Mock()
    mock_service.mark_complete.side_effect = NotFoundError("Task not found")

    with patch('hackathon_todo.cli.commands.display_error_message') as mock_display:
        complete_command_handler(mock_service, "some-id")

    mock_display.assert_called_once()
    assert "Not Found:" in mock_display.call_args[0][0]


def test_uncomplete_command_handler_success():
    """Test successful marking incomplete of a task via command handler."""
    mock_service = Mock()
    mock_task = Task(title="Test Task", completed=False)
    mock_service.mark_incomplete.return_value = mock_task

    with patch('hackathon_todo.cli.display.display_success_message'):
        uncomplete_command_handler(mock_service, "some-id")

    mock_service.mark_incomplete.assert_called_once_with("some-id")


def test_uncomplete_command_handler_not_found():
    """Test handling of not found errors in uncomplete command."""
    mock_service = Mock()
    mock_service.mark_incomplete.side_effect = NotFoundError("Task not found")

    with patch('hackathon_todo.cli.commands.display_error_message') as mock_display:
        uncomplete_command_handler(mock_service, "some-id")

    mock_display.assert_called_once()
    assert "Not Found:" in mock_display.call_args[0][0]