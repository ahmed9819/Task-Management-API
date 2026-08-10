from uuid import UUID

from fastapi import Depends, APIRouter, status

from app.dependencies.auth import get_current_user
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
    current_user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):

    user_id = UUID(current_user["sub"])

    return await service.create_task(
        task_data,
        user_id,
    )


@router.get(
    "",
    response_model=list[TaskResponse],
)
async def get_all_tasks(
    current_user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):

    user_id = UUID(current_user["sub"])

    return await service.get_all_tasks(
        user_id,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
async def get_task_by_id(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):

    user_id = UUID(current_user["sub"])

    return await service.get_task_by_id(
        task_id,
        user_id,
    )


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):

    user_id = UUID(current_user["sub"])

    return await service.update_task(
        task_id,
        task_data,
        user_id,
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):

    user_id = UUID(current_user["sub"])

    await service.delete_task(
        task_id,
        user_id,
    )