from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.repositories.task import TaskRepository
from app.services.task_service import TaskService


def get_task_repository(
    db: AsyncSession = Depends(get_db),
) -> TaskRepository:
    return TaskRepository(db)

def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
) -> TaskService:
    from app.services.task_service import TaskService
    return TaskService(repository)