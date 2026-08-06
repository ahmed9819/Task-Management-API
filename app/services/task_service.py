from app.models.task import Task
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate
from fastapi import HTTPException, status


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(
        self,
        task_data: TaskCreate,
    ) -> Task:
        return await self.repository.create(task_data)

    async def get_task_by_id(
        self,
        task_id: int,
    ) -> Task:
        task = await self.repository.get_by_id(task_id)

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found",
            )

        return task

    async def get_all_tasks(
        self,
    ) -> list[Task]:

        tasks = await self.repository.get_all()

        return tasks

    async def update_task(
        self,
        task_id: int,
        task_data: TaskUpdate,
    ) -> Task:
        task = await self.get_task_by_id(task_id)
        updated_task = await self.repository.update(task, task_data)

        return updated_task

    async def delete_task(
        self,
        task_id: int,
    ) -> None:
        task = await self.get_task_by_id(task_id)
        await self.repository.delete(task)