"""HTTP DELETE: удаление по id с проверкой владельца в core."""

from fastapi import APIRouter, Depends

from config import oauth2_scheme
from core.time.delete_time_core import (
    delete_daily_plan_implementation,
    delete_label_implementation,
    delete_project_implementation,
    delete_reminder_implementation,
    delete_task_implementation,
    delete_time_entry_implementation,
)
from templates.base_models.app_user import DefaultResponseModel

delete_time_router = APIRouter()


@delete_time_router.delete(
    "/projects/{project_id}",
    response_model=DefaultResponseModel,
    description="Удалить проект",
)
async def delete_project(project_id: int, token: str = Depends(oauth2_scheme)):
    return await delete_project_implementation(project_id=project_id, token=token)


@delete_time_router.delete(
    "/tasks/{task_id}",
    response_model=DefaultResponseModel,
    description="Удалить задачу",
)
async def delete_task(task_id: int, token: str = Depends(oauth2_scheme)):
    return await delete_task_implementation(task_id=task_id, token=token)


@delete_time_router.delete(
    "/time-entries/{time_entry_id}",
    response_model=DefaultResponseModel,
    description="Удалить запись времени",
)
async def delete_time_entry(time_entry_id: int, token: str = Depends(oauth2_scheme)):
    return await delete_time_entry_implementation(time_entry_id=time_entry_id, token=token)


@delete_time_router.delete(
    "/reminders/{reminder_id}",
    response_model=DefaultResponseModel,
    description="Удалить напоминание",
)
async def delete_reminder(reminder_id: int, token: str = Depends(oauth2_scheme)):
    return await delete_reminder_implementation(reminder_id=reminder_id, token=token)


@delete_time_router.delete(
    "/daily-plans/{daily_plan_id}",
    response_model=DefaultResponseModel,
    description="Удалить дневной план",
)
async def delete_daily_plan(daily_plan_id: int, token: str = Depends(oauth2_scheme)):
    return await delete_daily_plan_implementation(daily_plan_id=daily_plan_id, token=token)


@delete_time_router.delete(
    "/tags/{label_id}", response_model=DefaultResponseModel, description="Удалить тег"
)
async def delete_label(label_id: int, token: str = Depends(oauth2_scheme)):
    return await delete_label_implementation(label_id=label_id, token=token)
