"""
Бизнес-логика чтения (GET) для домена тайм-менеджера.

Все списки фильтруются по текущему пользователю из JWT.
"""

from models.main_tm_daily_plan_model import DailyPlan
from models.main_tm_project_model import Project
from models.main_tm_reminder_model import Reminder
from models.main_tm_task_model import Task
from models.main_tm_time_entry_model import Label, TimeEntry
from templates.base_models.time_daily_plan import DailyPlanListResponse, DailyPlanModel
from templates.base_models.time_entry import TimeEntryListResponse, TimeEntryModel
from templates.base_models.time_label import LabelListResponse, LabelModel
from templates.base_models.time_project import ProjectListResponse, ProjectModel
from templates.base_models.time_reminder import ReminderListResponse, ReminderModel
from templates.base_models.time_task import TaskListResponse, TaskModel
from logs.log_worker import custom_core_decorator

from config import database_engine_async
from utils.internal_workers.auth_worker import AuthNamespace
from utils.internal_workers.database_worker import DatabaseWorkerAsync

database_worker = DatabaseWorkerAsync(database_engine_async)


async def get_current_user_id(token: str) -> int:
    """Извлекает id пользователя после проверки токена."""
    user = await AuthNamespace.get_current_user(token=token)
    return user.id


@custom_core_decorator
async def list_projects_implementation(token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_orm_select(
        cls_from=Project,
        where_params=[Project.user_id == user_id],
        order_by=[Project.id.asc()],
    )
    return ProjectListResponse(data=[ProjectModel(**row.as_dict()) for row in rows])


@custom_core_decorator
async def list_tasks_implementation(token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_orm_select(
        cls_from=Task,
        where_params=[Task.user_id == user_id],
        order_by=[Task.id.asc()],
    )
    return TaskListResponse(data=[TaskModel(**row.as_dict()) for row in rows])


@custom_core_decorator
async def list_time_entries_implementation(token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_orm_select(
        cls_from=TimeEntry,
        where_params=[TimeEntry.user_id == user_id],
        order_by=[TimeEntry.id.asc()],
    )
    return TimeEntryListResponse(data=[TimeEntryModel(**row.as_dict()) for row in rows])


@custom_core_decorator
async def list_reminders_implementation(token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_orm_select(
        cls_from=Reminder,
        where_params=[Reminder.user_id == user_id],
        order_by=[Reminder.id.asc()],
    )
    return ReminderListResponse(data=[ReminderModel(**row.as_dict()) for row in rows])


@custom_core_decorator
async def list_daily_plans_implementation(token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_orm_select(
        cls_from=DailyPlan,
        where_params=[DailyPlan.user_id == user_id],
        order_by=[DailyPlan.id.asc()],
    )
    return DailyPlanListResponse(data=[DailyPlanModel(**row.as_dict()) for row in rows])


@custom_core_decorator
async def list_labels_implementation(token: str):
    user_id = await get_current_user_id(token)
    rows = await database_worker.custom_orm_select(
        cls_from=Label, where_params=[Label.user_id == user_id], order_by=[Label.id.asc()]
    )
    return LabelListResponse(data=[LabelModel(**row.as_dict()) for row in rows])
