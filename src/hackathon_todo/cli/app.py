"""
Main CLI application.

This module sets up the main CLI application with all necessary components
and dependency injection.
"""

from __future__ import annotations

from .commands import cli, register_commands
from ..services.task_service import TaskService
from ..storage.in_memory_storage import InMemoryStorage


def create_app() -> tuple:
    """
    Create and configure the CLI application with dependencies.

    Returns:
        A tuple containing the CLI group and the task service
    """
    # Initialize storage
    storage = InMemoryStorage()

    # Initialize service
    service = TaskService(storage=storage)

    # Register commands with the CLI
    register_commands(cli, service)

    return cli, service


def main() -> None:
    """Entry point for the CLI application."""
    app, _ = create_app()
    app()