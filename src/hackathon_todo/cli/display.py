"""
Display module for formatted console output.

This module provides functions for displaying tasks in a formatted way
using the Rich library for enhanced console output.
"""

from __future__ import annotations

from typing import List

from rich.console import Console
from rich.table import Table

from ..domain.models import Task


def display_tasks_table(tasks: List[Task]) -> None:
    """
    Display a list of tasks in a formatted table.

    Args:
        tasks: List of tasks to display
    """
    console = Console()

    if not tasks:
        console.print("[bold yellow]No tasks found.[/bold yellow]")
        return

    table = Table(title="Your Tasks")
    table.add_column("ID", style="dim", width=36)
    table.add_column("Title", style="bold")
    table.add_column("Status", justify="center")
    table.add_column("Created At", justify="center")

    for task in tasks:
        status = "[green]Done[/green]" if task.completed else "[yellow]Pending[/yellow]"
        table.add_row(
            task.id,
            task.title,
            status,
            task.created_at.strftime("%Y-%m-%d %H:%M")
        )

    console.print(table)


def display_task_detail(task: Task) -> None:
    """
    Display detailed information about a single task.

    Args:
        task: The task to display
    """
    console = Console()

    status = "Done" if task.completed else "Pending"

    console.print(f"[bold]{task.title}[/bold]")
    console.print(f"ID: {task.id}")
    console.print(f"Status: {status}")
    console.print(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
    console.print(f"Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M')}")

    if task.description:
        console.print("\n[bold]Description:[/bold]")
        console.print(task.description)


def display_success_message(message: str) -> None:
    """
    Display a success message in green.

    Args:
        message: The success message to display
    """
    console = Console()
    console.print(f"[green]SUCCESS: {message}[/green]")


def display_error_message(message: str) -> None:
    """
    Display an error message in red.

    Args:
        message: The error message to display
    """
    console = Console()
    console.print(f"[red]ERROR: {message}[/red]")


def display_info_message(message: str) -> None:
    """
    Display an informational message in blue.

    Args:
        message: The informational message to display
    """
    console = Console()
    console.print(f"[blue]INFO: {message}[/blue]")