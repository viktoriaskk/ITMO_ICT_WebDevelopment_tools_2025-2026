"""
HTTP GET для тайм-менеджера: списки проектов, задач, записей времени, напоминаний, планов, тегов.

Все маршруты защищены OAuth2 Bearer (см. oauth2_scheme).
"""

from fastapi import APIRouter, Depends

from config import oauth2_scheme
from core.time.get_time_core import (
    list_daily_plans_implementation,
    list_labels_implementation,
    list_projects_implementation,
    list_reminders_implementation,
    list_tasks_implementation,
    list_time_entries_implementation,
)
from templates.base_models.time_daily_plan import DailyPlanListResponse
from templates.base_models.time_entry import TimeEntryListResponse
from templates.base_models.time_label import LabelListResponse
from templates.base_models.time_project import ProjectListResponse
from templates.base_models.time_reminder import ReminderListResponse
from templates.base_models.time_task import TaskListResponse

get_time_router = APIRouter()


@get_time_router.get(
    "/projects",
    response_model=ProjectListResponse,
    description="Получить список проектов пользователя",
)
async def get_projects(token: str = Depends(oauth2_scheme)):
    return await list_projects_implementation(token=token)


@get_time_router.get(
    "/tasks",
    response_model=TaskListResponse,
    description="Получить список задач пользователя",
)
async def get_tasks(token: str = Depends(oauth2_scheme)):
    return await list_tasks_implementation(token=token)


@get_time_router.get(
    "/time-entries",
    response_model=TimeEntryListResponse,
    description="Получить список записей времени пользователя",
)
async def get_time_entries(token: str = Depends(oauth2_scheme)):
    return await list_time_entries_implementation(token=token)


@get_time_router.get(
    "/reminders",
    response_model=ReminderListResponse,
    description="Получить список напоминаний по задачам",
)
async def get_reminders(token: str = Depends(oauth2_scheme)):
    return await list_reminders_implementation(token=token)


@get_time_router.get(
    "/daily-plans",
    response_model=DailyPlanListResponse,
    description="Получить список дневных планов пользователя",
)
async def get_daily_plans(token: str = Depends(oauth2_scheme)):
    return await list_daily_plans_implementation(token=token)


@get_time_router.get(
    "/tags",
    response_model=LabelListResponse,
    description="Получить список тегов пользователя",
)
async def get_labels(token: str = Depends(oauth2_scheme)):
    return await list_labels_implementation(token=token)
