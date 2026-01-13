"""
Command handlers for the CLI application.

This module contains all the command handlers that interact with the TaskService
to perform various operations.
"""

from __future__ import annotations

import click
import cmd
import shlex
import sys

from ..domain.exceptions import NotFoundError, ValidationError
from ..domain.models import Task
from ..services.task_service import TaskService
from .display import (
    display_error_message,
    display_info_message,
    display_success_message,
    display_task_detail,
    display_tasks_table,
)


def add_command_handler(service: TaskService, title: str, description: str = "") -> None:
    """
    Handler for the add command.

    Args:
        service: The task service to use
        title: The title of the task to add
        description: The optional description of the task to add
    """
    try:
        task = service.add_task(title=title, description=description)
        display_success_message(f"Task '{task.title}' created successfully with ID: {task.id}")
    except ValidationError as e:
        display_error_message(e.message)


def list_command_handler(service: TaskService, status: str = None) -> None:
    """
    Handler for the list command.

    Args:
        service: The task service to use
        status: The status to filter by (optional)
    """
    try:
        if status:
            # Filter tasks by status
            all_tasks = service.get_all_tasks()
            if status.lower() == 'pending':
                tasks = [task for task in all_tasks if not task.completed]
            elif status.lower() == 'completed':
                tasks = [task for task in all_tasks if task.completed]
            else:
                display_error_message(f"Invalid status: {status}. Use 'pending' or 'completed'.")
                return
        else:
            tasks = service.get_all_tasks()
        display_tasks_table(tasks)
    except Exception as e:
        display_error_message(f"Error retrieving tasks: {str(e)}")


def view_command_handler(service: TaskService, task_id: str) -> None:
    """
    Handler for viewing a specific task.

    Args:
        service: The task service to use
        task_id: The ID of the task to view
    """
    try:
        task = service.get_task_by_id(task_id)
        display_task_detail(task)
    except NotFoundError as e:
        display_error_message(e.message)


def update_command_handler(service: TaskService, task_id: str, title: str = None, description: str = None) -> None:
    """
    Handler for the update command.

    Args:
        service: The task service to use
        task_id: The ID of the task to update
        title: The new title for the task (optional)
        description: The new description for the task (optional)
    """
    try:
        task = service.update_task(task_id=task_id, title=title, description=description)
        display_success_message(f"Task '{task.title}' updated successfully")
    except NotFoundError as e:
        display_error_message(e.message)
    except ValidationError as e:
        display_error_message(e.message)


def delete_command_handler(service: TaskService, task_id: str) -> None:
    """
    Handler for the delete command.

    Args:
        service: The task service to use
        task_id: The ID of the task to delete
    """
    try:
        service.delete_task(task_id)
        display_success_message("Task deleted successfully")
    except NotFoundError as e:
        display_error_message(e.message)


def complete_command_handler(service: TaskService, task_id: str) -> None:
    """
    Handler for the complete command.

    Args:
        service: The task service to use
        task_id: The ID of the task to mark complete
    """
    try:
        task = service.mark_complete(task_id)
        display_success_message(f"Task '{task.title}' marked as complete")
    except NotFoundError as e:
        display_error_message(e.message)


def uncomplete_command_handler(service: TaskService, task_id: str) -> None:
    """
    Handler for the uncomplete command.

    Args:
        service: The task service to use
        task_id: The ID of the task to mark incomplete
    """
    try:
        task = service.mark_incomplete(task_id)
        display_success_message(f"Task '{task.title}' marked as incomplete")
    except NotFoundError as e:
        display_error_message(e.message)


def shell_command_handler(service: TaskService) -> None:
    """
    Handler for the shell command.

    Args:
        service: The task service to use (will persist in the shell session)
    """
    shell = TodoShell(service)
    shell.cmdloop()


class TodoShell(cmd.Cmd):
    """
    Interactive shell for the Todo application.
    """

    intro = 'Todo App v1.0 - Type \'help\' for commands, \'exit\' to quit\n'
    prompt = '> '

    def __init__(self, service: TaskService):
        super().__init__()
        self.service = service

    def do_add(self, arg: str) -> bool:
        """
        Add a new task: add "title" --description "description"
        """
        try:
            args = shlex.split(arg)
            if not args:
                display_error_message("Title is required")
                return False

            title = args[0]
            description = ""

            # Parse --description if present
            i = 1
            while i < len(args):
                if args[i] == "--description" and i + 1 < len(args):
                    description = args[i + 1]
                    i += 2
                else:
                    i += 1

            task = self.service.add_task(title=title, description=description)
            display_success_message(f"Task '{task.title}' created successfully with ID: {task.id}")
            print(f"(Note: Use full ID '{task.id}' for other commands)")
        except Exception as e:
            display_error_message(str(e))

        return False

    def do_list(self, arg: str) -> bool:
        """
        List all tasks: list [--status pending|completed]
        """
        try:
            # Parse --status if present
            args = shlex.split(arg)
            status = None

            i = 0
            while i < len(args):
                if args[i] == "--status" and i + 1 < len(args):
                    status = args[i + 1]
                    break
                i += 1

            # Call the same handler used by the regular list command
            list_command_handler(self.service, status)
        except Exception as e:
            display_error_message(str(e))

        return False

    def do_view(self, arg: str) -> bool:
        """
        View a specific task: view <task_id>
        """
        try:
            args = shlex.split(arg)
            if not args:
                display_error_message("Task ID is required")
                return False

            task_id = args[0]
            view_command_handler(self.service, task_id)
        except Exception as e:
            display_error_message(str(e))

        return False

    def do_update(self, arg: str) -> bool:
        """
        Update a task: update <task_id> [--title "new_title"] [--description "new_description"]
        """
        try:
            args = shlex.split(arg)
            if not args:
                display_error_message("Task ID is required")
                return False

            task_id = args[0]
            title = None
            description = None

            # Parse --title and --description if present
            i = 1
            while i < len(args):
                if args[i] == "--title" and i + 1 < len(args):
                    title = args[i + 1]
                    i += 2
                elif args[i] == "--description" and i + 1 < len(args):
                    description = args[i + 1]
                    i += 2
                else:
                    i += 1

            update_command_handler(self.service, task_id, title, description)
        except Exception as e:
            display_error_message(str(e))

        return False

    def do_delete(self, arg: str) -> bool:
        """
        Delete a task: delete <task_id>
        """
        try:
            args = shlex.split(arg)
            if not args:
                display_error_message("Task ID is required")
                return False

            task_id = args[0]
            delete_command_handler(self.service, task_id)
        except Exception as e:
            display_error_message(str(e))

        return False

    def do_complete(self, arg: str) -> bool:
        """
        Mark a task as complete: complete <task_id>
        """
        try:
            args = shlex.split(arg)
            if not args:
                display_error_message("Task ID is required")
                return False

            task_id = args[0]
            complete_command_handler(self.service, task_id)
        except Exception as e:
            display_error_message(str(e))

        return False

    def do_uncomplete(self, arg: str) -> bool:
        """
        Mark a task as incomplete: uncomplete <task_id>
        """
        try:
            args = shlex.split(arg)
            if not args:
                display_error_message("Task ID is required")
                return False

            task_id = args[0]
            uncomplete_command_handler(self.service, task_id)
        except Exception as e:
            display_error_message(str(e))

        return False

    def do_exit(self, arg: str) -> bool:
        """
        Exit the shell: exit
        """
        print("Goodbye!")
        return True

    def do_quit(self, arg: str) -> bool:
        """
        Quit the shell: quit
        """
        return self.do_exit(arg)

    def emptyline(self) -> bool:
        """
        Handle empty line input
        """
        return False

    def default(self, line: str) -> bool:
        """
        Handle unknown commands
        """
        print(f"Unknown command: {line.split()[0] if line.split() else ''}")
        print("Type 'help' for available commands")
        return False


# Click command definitions
@click.group()
def cli():
    """Console application for managing todo tasks."""
    pass


def register_commands(cli, service: TaskService):
    """
    Register all commands with the CLI group.

    Args:
        cli: The CLI group to register commands with
        service: The task service to use in command handlers
    """

    @cli.command()
    @click.argument('title', type=str)
    @click.option('--description', default='', help='Description of the task')
    def add(title: str, description: str):
        """Add a new task."""
        add_command_handler(service, title, description)

    @cli.command()
    @click.option('--status', type=click.Choice(['pending', 'completed']), help='Filter tasks by status')
    def list(status: str = None):
        """List all tasks."""
        list_command_handler(service, status)

    @cli.command()
    @click.argument('task_id')
    def view(task_id: str):
        """View a specific task."""
        view_command_handler(service, task_id)

    @cli.command()
    @click.argument('task_id')
    @click.option('--title', help='New title for the task')
    @click.option('--description', help='New description for the task')
    def update(task_id: str, title: str = None, description: str = None):
        """Update a task."""
        update_command_handler(service, task_id, title, description)

    @cli.command()
    @click.argument('task_id')
    def delete(task_id: str):
        """Delete a task."""
        delete_command_handler(service, task_id)

    @cli.command()
    @click.argument('task_id')
    def complete(task_id: str):
        """Mark a task as complete."""
        complete_command_handler(service, task_id)

    @cli.command()
    @click.argument('task_id')
    def uncomplete(task_id: str):
        """Mark a task as incomplete."""
        uncomplete_command_handler(service, task_id)

    @cli.command()
    def shell():
        """Start an interactive shell."""
        shell_command_handler(service)