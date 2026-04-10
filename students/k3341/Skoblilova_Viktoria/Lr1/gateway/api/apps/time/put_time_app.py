"""HTTP PUT: частичное обновление полей (exclude_unset в core)."""

from fastapi import APIRouter, Depends

from config import oauth2_scheme
from core.time.put_time_core import (
    update_daily_plan_implementation,
    update_label_implementation,
    update_project_implementation,
    update_reminder_implementation,
    update_task_implementation,
    update_time_entry_implementation,
)
from templates.base_models.time_daily_plan import DailyPlanModel
from templates.base_models.time_entry import TimeEntryModel
from templates.base_models.time_label import LabelModel
from templates.base_models.time_project import ProjectModel
from templates.base_models.time_reminder import ReminderModel
from templates.base_models.time_task import TaskModel
from templates.base_models.time_update import (
    DailyPlanUpdateRequest,
    LabelUpdateRequest,
    ProjectUpdateRequest,
    ReminderUpdateRequest,
    TaskUpdateRequest,
    TimeEntryUpdateRequest,
)

put_time_router = APIRouter()


@put_time_router.put("/projects/{project_id}", response_model=ProjectModel, description="Обновить проект")
async def put_project(
    project_id: int, data: ProjectUpdateRequest, token: str = Depends(oauth2_scheme)
):
    return await update_project_implementation(project_id=project_id, data=data, token=token)


@put_time_router.put("/tasks/{task_id}", response_model=TaskModel, description="Обновить задачу")
async def put_task(task_id: int, data: TaskUpdateRequest, token: str = Depends(oauth2_scheme)):
    return await update_task_implementation(task_id=task_id, data=data, token=token)


@put_time_router.put(
    "/time-entries/{time_entry_id}",
    response_model=TimeEntryModel,
    description="Обновить запись времени",
)
async def put_time_entry(
    time_entry_id: int, data: TimeEntryUpdateRequest, token: str = Depends(oauth2_scheme)
):
    return await update_time_entry_implementation(
        time_entry_id=time_entry_id, data=data, token=token
    )


@put_time_router.put("/reminders/{reminder_id}", response_model=ReminderModel, description="Обновить напоминание")
async def put_reminder(
    reminder_id: int, data: ReminderUpdateRequest, token: str = Depends(oauth2_scheme)
):
    return await update_reminder_implementation(
        reminder_id=reminder_id, data=data, token=token
    )


@put_time_router.put("/daily-plans/{daily_plan_id}", response_model=DailyPlanModel, description="Обновить дневной план")
async def put_daily_plan(
    daily_plan_id: int, data: DailyPlanUpdateRequest, token: str = Depends(oauth2_scheme)
):
    return await update_daily_plan_implementation(
        daily_plan_id=daily_plan_id, data=data, token=token
    )


@put_time_router.put("/tags/{label_id}", response_model=LabelModel, description="Обновить тег")
async def put_label(
    label_id: int, data: LabelUpdateRequest, token: str = Depends(oauth2_scheme)
):
    return await update_label_implementation(label_id=label_id, data=data, token=token)
