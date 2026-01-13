"""
Custom exception classes for the Hackathon Todo application.

This module defines the exception hierarchy for proper error handling
throughout the application.
"""

from __future__ import annotations


class TodoAppError(Exception):
    """Base exception class for all application-specific errors."""

    def __init__(self, message: str) -> None:
        """
        Initialize the exception with a message.

        Args:
            message: Human-readable error description
        """
        self.message = message
        super().__init__(self.message)


class ValidationError(TodoAppError):
    """Raised when input validation fails."""

    def __init__(self, message: str) -> None:
        """
        Initialize the validation error with a message.

        Args:
            message: Description of the validation failure
        """
        super().__init__(f"Validation Error: {message}")


class NotFoundError(TodoAppError):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str) -> None:
        """
        Initialize the not found error with a message.

        Args:
            message: Description of the missing resource
        """
        super().__init__(f"Not Found: {message}")


class StorageError(TodoAppError):
    """Raised when storage operations fail."""

    def __init__(self, message: str) -> None:
        """
        Initialize the storage error with a message.

        Args:
            message: Description of the storage failure
        """
        super().__init__(f"Storage Error: {message}")