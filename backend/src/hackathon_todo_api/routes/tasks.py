from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from ..services.task_service import (
    get_tasks, get_task_by_id, create_task, update_task,
    delete_task, toggle_task_completion
)
from ..schemas.task import TaskCreate, TaskRead, TaskUpdate, TaskToggleComplete
from ..auth.jwt import get_current_user

router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[TaskRead])
async def read_tasks(
    user_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """
    Retrieve all tasks for the specified user
    """
    # Verify that the requesting user is the same as the user in the path
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's tasks"
        )

    tasks = await get_tasks(current_user_id)
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    user_id: str,
    task: TaskCreate,
    current_user_id: str = Depends(get_current_user)
):
    """
    Create a new task for the specified user
    """
    # Verify that the requesting user is the same as the user in the path
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    return await create_task(task, current_user_id)


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskRead)
async def read_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user)
):
    """
    Retrieve a specific task by ID for the specified user
    """
    # Verify that the requesting user is the same as the user in the path
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's tasks"
        )

    task = await get_task_by_id(task_id, current_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead)
async def update_existing_task(
    user_id: str,
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user)
):
    """
    Update a specific task by ID for the specified user
    """
    # Verify that the requesting user is the same as the user in the path
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's tasks"
        )

    updated_task = await update_task(task_id, task_update, current_user_id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    return updated_task


@router.delete("/{user_id}/tasks/{task_id}")
async def delete_existing_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user)
):
    """
    Delete a specific task by ID for the specified user
    """
    # Verify that the requesting user is the same as the user in the path
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user's tasks"
        )

    deleted = await delete_task(task_id, current_user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskRead)
async def toggle_task_complete(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user)
):
    """
    Toggle the completion status of a specific task for the specified user
    """
    # Verify that the requesting user is the same as the user in the path
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's tasks"
        )

    updated_task = await toggle_task_completion(task_id, current_user_id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    return updated_task