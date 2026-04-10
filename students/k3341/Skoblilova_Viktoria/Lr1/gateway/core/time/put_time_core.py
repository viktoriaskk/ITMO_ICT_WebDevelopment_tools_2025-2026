"""Бизнес-логика обновления (PUT) сущностей тайм-менеджера для текущего пользователя."""

from fastapi import HTTPException

from models.main_tm_daily_plan_model import DailyPlan
from models.main_tm_project_model import Project
from models.main_tm_reminder_model import Reminder
from models.main_tm_task_model import Task
from models.main_tm_time_entry_model import Label, TimeEntry
from templates.base_models.time_daily_plan import DailyPlanModel
from templates.base_models.time_entry import TimeEntryModel
from templates.base_models.time_label import LabelModel
from templates.base_models.time_project import ProjectModel
from templates.base_models.time_reminder import ReminderModel
from templates.base_models.time_task import TaskModel
from logs.log_worker import custom_core_decorator

from config import database_engine_async
from utils.internal_workers.auth_worker import AuthNamespace
from utils.internal_workers.database_worker import DatabaseWorkerAsync

database_worker = DatabaseWorkerAsync(database_engine_async)


async def get_current_user_id(token: str) -> int:
    user = await AuthNamespace.get_current_user(token=token)
    return user.id


@custom_core_decorator
async def update_project_implementation(project_id: int, data, token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_update(
        cls_to=Project,
        where_params=[Project.id == project_id, Project.user_id == user_id],
        data=data.model_dump(exclude_unset=True),
        returning=Project,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectModel(**rows[0].as_dict())


@custom_core_decorator
async def update_task_implementation(task_id: int, data, token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_update(
        cls_to=Task,
        where_params=[Task.id == task_id, Task.user_id == user_id],
        data=data.model_dump(exclude_unset=True),
        returning=Task,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskModel(**rows[0].as_dict())


@custom_core_decorator
async def update_time_entry_implementation(time_entry_id: int, data, token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_update(
        cls_to=TimeEntry,
        where_params=[TimeEntry.id == time_entry_id, TimeEntry.user_id == user_id],
        data=data.model_dump(exclude_unset=True),
        returning=TimeEntry,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Time entry not found")
    return TimeEntryModel(**rows[0].as_dict())


@custom_core_decorator
async def update_reminder_implementation(reminder_id: int, data, token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_update(
        cls_to=Reminder,
        where_params=[Reminder.id == reminder_id, Reminder.user_id == user_id],
        data=data.model_dump(exclude_unset=True),
        returning=Reminder,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return ReminderModel(**rows[0].as_dict())


@custom_core_decorator
async def update_daily_plan_implementation(daily_plan_id: int, data, token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_update(
        cls_to=DailyPlan,
        where_params=[DailyPlan.id == daily_plan_id, DailyPlan.user_id == user_id],
        data=data.model_dump(exclude_unset=True),
        returning=DailyPlan,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Daily plan not found")
    return DailyPlanModel(**rows[0].as_dict())


@custom_core_decorator
async def update_label_implementation(label_id: int, data, token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_update(
        cls_to=Label,
        where_params=[Label.id == label_id, Label.user_id == user_id],
        data=data.model_dump(exclude_unset=True),
        returning=Label,
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Tag not found")
    return LabelModel(**rows[0].as_dict())
