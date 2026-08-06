from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self, 
        task_data: TaskCreate,
    ) -> Task:
        task = Task(**task_data.model_dump())
            
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)

        return task

    async def get_by_id(
        self,
        task_id: int, 
    ) -> Task | None:
        
        return await self.db.get(Task, task_id)
        
    async def get_all(self) -> list[Task]:

        result = await self.db.execute(
        select(Task)
    )

        tasks = result.scalars().all()

        return tasks

    async def update(
        self,
        task: Task,
        task_data: TaskUpdate,
    ) -> Task:

        update_data = task_data.model_dump(exclude_unset=True)

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

