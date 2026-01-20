from typing import List, Optional
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from ..database import AsyncSessionLocal
from ..models.task import Task, TaskUpdate as TaskUpdateModel
from ..models.user import User
from ..schemas.task import TaskCreate, TaskRead, TaskUpdate


async def get_tasks(user_id: str) -> List[TaskRead]:
    async with AsyncSessionLocal() as session:
        statement = select(Task).where(Task.user_id == user_id)
        result = await session.execute(statement)
        tasks = result.scalars().all()

        # Convert to TaskRead objects
        task_reads = []
        for task in tasks:
            task_read = TaskRead(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                user_id=task.user_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            task_reads.append(task_read)
        return task_reads


async def get_task_by_id(task_id: int, user_id: str) -> Optional[TaskRead]:
    async with AsyncSessionLocal() as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if task:
            return TaskRead(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                user_id=task.user_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
        return None


async def create_task(task_data: TaskCreate, user_id: str) -> TaskRead:
    async with AsyncSessionLocal() as session:
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=False,
            user_id=user_id
        )
        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)

        return TaskRead(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            completed=db_task.completed,
            user_id=db_task.user_id,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at
        )


async def update_task(task_id: int, task_update: TaskUpdate, user_id: str) -> Optional[TaskRead]:
    async with AsyncSessionLocal() as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return None

        # Update the task with provided fields
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(task, field) and value is not None:
                setattr(task, field, value)

        # Update the updated_at timestamp
        from datetime import datetime
        task.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(task)

        return TaskRead(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )


async def delete_task(task_id: int, user_id: str) -> bool:
    async with AsyncSessionLocal() as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return False

        await session.delete(task)
        await session.commit()
        return True


async def toggle_task_completion(task_id: int, user_id: str) -> Optional[TaskRead]:
    async with AsyncSessionLocal() as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return None

        task.completed = not task.completed
        from datetime import datetime
        task.updated_at = datetime.utcnow()  # Update the timestamp
        await session.commit()
        await session.refresh(task)

        return TaskRead(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )