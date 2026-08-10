from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        task_data: TaskCreate,
        user_id: UUID,
    ) -> Task:

        task = Task(
            **task_data.model_dump(),
            user_id=user_id,
        )

        self.db.add(task)

        await self.db.commit()
        await self.db.refresh(task)

        return task

    async def get_by_id(
        self,
        task_id: int,
        user_id: UUID,
    ) -> Task | None:

        result = await self.db.execute(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_all(
        self,
        user_id: UUID,
    ) -> list[Task]:

        result = await self.db.execute(
            select(Task).where(
                Task.user_id == user_id,
            )
        )

        return list(result.scalars().all())

    async def update(
        self,
        task: Task,
        task_data: TaskUpdate,
    ) -> Task:

        update_data = task_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(task, field, value)

        await self.db.commit()
        await self.db.refresh(task)

        return task

    async def delete(
        self,
        task: Task,
    ) -> None:

        await self.db.delete(task)
        await self.db.commit()

