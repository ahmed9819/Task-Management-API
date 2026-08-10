from uuid import UUID

from fastapi import HTTPException, status

from app.models.task import Task
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(
        self,
        task_data: TaskCreate,
        user_id: UUID,
    ) -> Task:

        return await self.repository.create(
            task_data,
            user_id,
        )

    async def get_task_by_id(
        self,
        task_id: int,
        user_id: UUID,
    ) -> Task:

        task = await self.repository.get_by_id(
            task_id,
            user_id,
        )

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found",
            )

        return task

    async def get_all_tasks(
        self,
        user_id: UUID,
    ) -> list[Task]:

        return await self.repository.get_all(user_id)

    async def update_task(
        self,
        task_id: int,
        task_data: TaskUpdate,
        user_id: UUID,
    ) -> Task:

        task = await self.get_task_by_id(
            task_id,
            user_id,
        )

        return await self.repository.update(
            task,
            task_data,
        )

    async def delete_task(
        self,
        task_id: int,
        user_id: UUID,
    ) -> None:

        task = await self.get_task_by_id(
            task_id,
            user_id,
        )

        await self.repository.delete(task)