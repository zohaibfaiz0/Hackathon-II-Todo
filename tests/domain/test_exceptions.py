"""
Tests for domain exceptions.

This module contains tests for custom exception classes.
Tests achieve 100% coverage for the domain exceptions.
"""

import pytest
from hackathon_todo.domain.exceptions import TodoAppError, ValidationError, NotFoundError, StorageError


def test_todoapp_error_initialization():
    """Test initializing TodoAppError with a message."""
    error = TodoAppError("Test error message")
    assert str(error) == "Test error message"
    assert error.message == "Test error message"


def test_validation_error_initialization():
    """Test initializing ValidationError with a message."""
    error = ValidationError("Invalid input")
    assert "Validation Error: Invalid input" in str(error)


def test_not_found_error_initialization():
    """Test initializing NotFoundError with a message."""
    error = NotFoundError("Item not found")
    assert "Not Found: Item not found" in str(error)


def test_storage_error_initialization():
    """Test initializing StorageError with a message."""
    error = StorageError("Storage operation failed")
    assert "Storage Error: Storage operation failed" in str(error)


def test_exception_inheritance():
    """Test that all custom exceptions inherit from TodoAppError."""
    validation_error = ValidationError("test")
    not_found_error = NotFoundError("test")
    storage_error = StorageError("test")

    assert isinstance(validation_error, TodoAppError)
    assert isinstance(not_found_error, TodoAppError)
    assert isinstance(storage_error, TodoAppError)