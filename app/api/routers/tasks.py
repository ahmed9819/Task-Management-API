from fastapi import Depends, APIRouter, status

from app.dependencies.task import get_task_service
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service),
):
    return await service.create_task(task_data)


@router.get(
    "",
    response_model=list[TaskResponse],
)
async def get_all_tasks(
    service: TaskService = Depends(get_task_service),
):
    return await service.get_all_tasks()


@router.get("/{task_id}")
async def get_task_by_id(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):

    return await service.get_task_by_id(task_id)


@router.patch("/{task_id}")
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):

    return await service.update_task(
        task_id,
        task_data
    )

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):

    return await service.delete_task(task_id)