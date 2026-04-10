"""Бизнес-логика удаления (DELETE); операции ограничены user_id из JWT."""

from models.main_tm_daily_plan_model import DailyPlan
from models.main_tm_project_model import Project
from models.main_tm_reminder_model import Reminder
from models.main_tm_task_model import Task
from models.main_tm_time_entry_model import Label, TimeEntry
from templates.base_models.app_user import DefaultResponseModel
from logs.log_worker import custom_core_decorator

from config import database_engine_async
from utils.internal_workers.auth_worker import AuthNamespace
from utils.internal_workers.database_worker import DatabaseWorkerAsync

database_worker = DatabaseWorkerAsync(database_engine_async)


async def get_current_user_id(token: str) -> int:
    user = await AuthNamespace.get_current_user(token=token)
    return user.id


@custom_core_decorator
async def delete_project_implementation(project_id: int, token: str):
    user_id = await get_current_user_id(token)
    await database_worker.custom_delete_all(
        cls_from=Project,
        where_params=[Project.id == project_id, Project.user_id == user_id],
    )
    return DefaultResponseModel(status="success", detail="Project deleted")


@custom_core_decorator
async def delete_task_implementation(task_id: int, token: str):
    user_id = await get_current_user_id(token)
    await database_worker.custom_delete_all(
        cls_from=Task,
        where_params=[Task.id == task_id, Task.user_id == user_id],
    )
    return DefaultResponseModel(status="success", detail="Task deleted")


@custom_core_decorator
async def delete_time_entry_implementation(time_entry_id: int, token: str):
    user_id = await get_current_user_id(token)
    await database_worker.custom_delete_all(
        cls_from=TimeEntry,
        where_params=[TimeEntry.id == time_entry_id, TimeEntry.user_id == user_id],
    )
    return DefaultResponseModel(status="success", detail="Time entry deleted")


@custom_core_decorator
async def delete_reminder_implementation(reminder_id: int, token: str):
    user_id = await get_current_user_id(token)
    await database_worker.custom_delete_all(
        cls_from=Reminder,
        where_params=[Reminder.id == reminder_id, Reminder.user_id == user_id],
    )
    return DefaultResponseModel(status="success", detail="Reminder deleted")


@custom_core_decorator
async def delete_daily_plan_implementation(daily_plan_id: int, token: str):
    user_id = await get_current_user_id(token)
    await database_worker.custom_delete_all(
        cls_from=DailyPlan,
        where_params=[DailyPlan.id == daily_plan_id, DailyPlan.user_id == user_id],
    )
    return DefaultResponseModel(status="success", detail="Daily plan deleted")


@custom_core_decorator
async def delete_label_implementation(label_id: int, token: str):
    user_id = await get_current_user_id(token)
    await database_worker.custom_delete_all(
        cls_from=Label, where_params=[Label.id == label_id, Label.user_id == user_id]
    )
    return DefaultResponseModel(status="success", detail="Tag deleted")
