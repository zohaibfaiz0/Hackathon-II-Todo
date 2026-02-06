from typing import List, Dict, Any, Optional

# Tool Schema Definitions
ADD_TASK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "add_task",
        "description": "Create a new task for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the task to create"
                },
                "description": {
                    "type": "string",
                    "description": "Optional description of the task"
                }
            },
            "required": ["title"]
        }
    }
}

LIST_TASKS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "list_tasks",
        "description": "List all tasks for the user, optionally filtered by status",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["all", "pending", "completed"],
                    "description": "Filter tasks by status. Default is 'all'"
                }
            },
            "required": []
        }
    }
}

COMPLETE_TASK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "complete_task",
        "description": "Mark a task as complete",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to mark as complete"
                }
            },
            "required": ["task_id"]
        }
    }
}

DELETE_TASK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "delete_task",
        "description": "Delete a task",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to delete"
                }
            },
            "required": ["task_id"]
        }
    }
}

UPDATE_TASK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "update_task",
        "description": "Update a task's title or description",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to update"
                },
                "title": {
                    "type": "string",
                    "description": "New title for the task"
                },
                "description": {
                    "type": "string",
                    "description": "New description for the task"
                }
            },
            "required": ["task_id"]
        }
    }
}


def get_all_tools() -> List[Dict[str, Any]]:
    """Return all tool schemas for OpenAI function calling."""
    return [
        ADD_TASK_SCHEMA,
        LIST_TASKS_SCHEMA,
        COMPLETE_TASK_SCHEMA,
        DELETE_TASK_SCHEMA,
        UPDATE_TASK_SCHEMA,
    ]


# Tool implementation functions (to be implemented in T-306 to T-310)
async def add_task_tool(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Create a new task for the user.

    Args:
        user_id: The ID of the user creating the task
        title: The title of the task
        description: Optional description of the task

    Returns:
        Dict with task_id, status, and title
    """
    try:
        from ..services.task_service import create_task
        from ..schemas.task import TaskCreate

        task_data = TaskCreate(
            title=title,
            description=description or ""
        )

        task = await create_task(task_data, user_id)

        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }


async def list_tasks_tool(user_id: str, status: str = "all") -> Dict[str, Any]:
    """List tasks for the user, optionally filtered by status.

    Args:
        user_id: The ID of the user
        status: Filter by status - "all", "pending", or "completed"

    Returns:
        Dict with tasks array and count
    """
    try:
        from ..services.task_service import get_tasks

        # Get all tasks for user
        tasks = await get_tasks(user_id)

        # Filter by status if needed
        if status == "pending":
            tasks = [t for t in tasks if not t.completed]
        elif status == "completed":
            tasks = [t for t in tasks if t.completed]
        # "all" returns everything

        # Convert to simple dict format for AI readability
        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description or "",
                "completed": task.completed,
            }
            for task in tasks
        ]

        return {
            "tasks": task_list,
            "count": len(task_list),
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed",
            "tasks": []
        }


async def complete_task_tool(user_id: str, task_id: int) -> Dict[str, Any]:
    """Mark a task as complete.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to complete

    Returns:
        Dict with task_id, status, and title
    """
    try:
        from ..services.task_service import toggle_task_completion

        task = await toggle_task_completion(task_id, user_id)

        if task is None:
            return {
                "error": f"Task with ID {task_id} not found",
                "status": "not_found"
            }

        return {
            "task_id": task.id,
            "status": "completed" if task.completed else "uncompleted",
            "title": task.title
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }


async def delete_task_tool(user_id: str, task_id: int) -> Dict[str, Any]:
    """Delete a task.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to delete

    Returns:
        Dict with task_id, status, and title
    """
    try:
        from ..services.task_service import delete_task, get_task_by_id

        # Get task info first (to return title after deletion)
        task = await get_task_by_id(task_id, user_id)

        if task is None:
            return {
                "error": f"Task with ID {task_id} not found",
                "status": "not_found"
            }

        # Store title before deletion
        task_title = task.title

        # Delete the task
        deleted = await delete_task(task_id, user_id)

        if not deleted:
            return {
                "error": f"Failed to delete task with ID {task_id}",
                "status": "failed"
            }

        return {
            "task_id": task_id,
            "status": "deleted",
            "title": task_title
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }


async def update_task_tool(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """Update a task's title or description.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)

    Returns:
        Dict with task_id, status, and title
    """
    try:
        from ..services.task_service import update_task
        from ..models.task import TaskUpdate

        # Build update data with only provided fields
        update_data = TaskUpdate()
        if title is not None:
            update_data.title = title
        if description is not None:
            update_data.description = description

        task = await update_task(task_id, update_data, user_id)

        if task is None:
            return {
                "error": f"Task with ID {task_id} not found",
                "status": "not_found"
            }

        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }


# Tool router
TOOL_FUNCTIONS = {
    "add_task": add_task_tool,
    "list_tasks": list_tasks_tool,
    "complete_task": complete_task_tool,
    "delete_task": delete_task_tool,
    "update_task": update_task_tool,
}


async def execute_tool(tool_name: str, user_id: str, **kwargs) -> Dict[str, Any]:
    """Execute a tool by name with the given arguments."""
    if tool_name not in TOOL_FUNCTIONS:
        return {"error": f"Unknown tool: {tool_name}", "status": "failed"}

    try:
        tool_func = TOOL_FUNCTIONS[tool_name]
        result = await tool_func(user_id=user_id, **kwargs)
        return result
    except NotImplementedError as e:
        return {"error": str(e), "status": "not_implemented"}
    except Exception as e:
        return {"error": str(e), "status": "failed"}