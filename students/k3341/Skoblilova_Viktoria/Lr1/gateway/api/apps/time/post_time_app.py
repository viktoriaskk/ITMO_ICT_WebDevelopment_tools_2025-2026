"""HTTP POST: создание сущностей и привязка тега к записи времени."""

from fastapi import APIRouter, Depends

from config import oauth2_scheme
from core.time.post_time_core import (
    bind_label_to_time_entry_implementation,
    create_daily_plan_implementation,
    create_label_implementation,
    create_project_implementation,
    create_reminder_implementation,
    create_task_implementation,
    create_time_entry_implementation,
)
from templates.base_models.app_user import DefaultResponseModel
from templates.base_models.time_daily_plan import DailyPlanCreateRequest, DailyPlanModel
from templates.base_models.time_entry import TimeEntryCreateRequest, TimeEntryModel
from templates.base_models.time_label import (
    LabelCreateRequest,
    LabelModel,
    TimeEntryLabelBindRequest,
)
from templates.base_models.time_project import ProjectCreateRequest, ProjectModel
from templates.base_models.time_reminder import ReminderCreateRequest, ReminderModel
from templates.base_models.time_task import TaskCreateRequest, TaskModel

post_time_router = APIRouter()


@post_time_router.post("/projects", response_model=ProjectModel, description="Создать новый проект")
async def post_project(data: ProjectCreateRequest, token: str = Depends(oauth2_scheme)):
    return await create_project_implementation(data=data, token=token)


@post_time_router.post("/tasks", response_model=TaskModel, description="Создать новую задачу")
async def post_task(data: TaskCreateRequest, token: str = Depends(oauth2_scheme)):
    return await create_task_implementation(data=data, token=token)


@post_time_router.post(
    "/time-entries",
    response_model=TimeEntryModel,
    description="Добавить запись потраченного времени",
)
async def post_time_entry(data: TimeEntryCreateRequest, token: str = Depends(oauth2_scheme)):
    return await create_time_entry_implementation(data=data, token=token)


@post_time_router.post("/reminders", response_model=ReminderModel, description="Создать напоминание")
async def post_reminder(data: ReminderCreateRequest, token: str = Depends(oauth2_scheme)):
    return await create_reminder_implementation(data=data, token=token)


@post_time_router.post("/daily-plans", response_model=DailyPlanModel, description="Создать дневной план")
async def post_daily_plan(data: DailyPlanCreateRequest, token: str = Depends(oauth2_scheme)):
    return await create_daily_plan_implementation(data=data, token=token)


@post_time_router.post("/tags", response_model=LabelModel, description="Создать тег")
async def post_label(data: LabelCreateRequest, token: str = Depends(oauth2_scheme)):
    return await create_label_implementation(data=data, token=token)


@post_time_router.post(
    "/time-entry-tags",
    response_model=DefaultResponseModel,
    description="Привязать тег к записи времени",
)
async def post_time_entry_tag(
    data: TimeEntryLabelBindRequest, token: str = Depends(oauth2_scheme)
):
    return await bind_label_to_time_entry_implementation(data=data, token=token)
