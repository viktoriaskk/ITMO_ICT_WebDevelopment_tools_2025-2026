"""
Бизнес-логика создания (POST): проекты, задачи, записи времени, напоминания, планы, теги.

Привязка тега к записи времени идёт через ассоциативную таблицу с relevance_score.
"""

from fastapi import HTTPException

from models.main_tm_daily_plan_model import DailyPlan
from models.main_tm_project_model import Project
from models.main_tm_reminder_model import Reminder
from models.main_tm_task_model import Task
from models.main_tm_time_entry_model import Label, M2M_TimeEntryLabel, TimeEntry
from templates.base_models.app_user import DefaultResponseModel
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
    """ID владельца данных по JWT (sub = email)."""
    user = await AuthNamespace.get_current_user(token=token)
    return user.id


@custom_core_decorator
async def create_project_implementation(data, token: str):
    user_id = await get_current_user_id(token)
    instance = Project(user_id=user_id, **data.model_dump())
    result = await database_worker.custom_insert(
        cls_to=Project,
        data=[instance.as_dict()],
        returning=Project,
        return_unpacked=True,
    )
    return ProjectModel(**result.as_dict())


@custom_core_decorator
async def create_task_implementation(data, token: str):
    user_id = await get_current_user_id(token)
    instance = Task(user_id=user_id, **data.model_dump())
    result = await database_worker.custom_insert(
        cls_to=Task,
        data=[instance.as_dict()],
        returning=Task,
        return_unpacked=True,
    )
    return TaskModel(**result.as_dict())


@custom_core_decorator
async def create_time_entry_implementation(data, token: str):
    user_id = await get_current_user_id(token)
    instance = TimeEntry(user_id=user_id, **data.model_dump(exclude_none=True))
    result = await database_worker.custom_insert(
        cls_to=TimeEntry,
        data=[instance.as_dict()],
        returning=TimeEntry,
        return_unpacked=True,
    )
    return TimeEntryModel(**result.as_dict())


@custom_core_decorator
async def create_reminder_implementation(data, token: str):
    user_id = await get_current_user_id(token)
    instance = Reminder(user_id=user_id, **data.model_dump())
    result = await database_worker.custom_insert(
        cls_to=Reminder,
        data=[instance.as_dict()],
        returning=Reminder,
        return_unpacked=True,
    )
    return ReminderModel(**result.as_dict())


@custom_core_decorator
async def create_daily_plan_implementation(data, token: str):
    user_id = await get_current_user_id(token)
    instance = DailyPlan(user_id=user_id, **data.model_dump(exclude_none=True))
    result = await database_worker.custom_insert(
        cls_to=DailyPlan,
        data=[instance.as_dict()],
        returning=DailyPlan,
        return_unpacked=True,
    )
    return DailyPlanModel(**result.as_dict())


@custom_core_decorator
async def create_label_implementation(data, token: str):
    user_id = await get_current_user_id(token)
    instance = Label(user_id=user_id, name=data.name)
    result = await database_worker.custom_insert(
        cls_to=Label, data=[instance.as_dict()], returning=Label, return_unpacked=True
    )
    return LabelModel(**result.as_dict())


@custom_core_decorator
async def bind_label_to_time_entry_implementation(data, token: str):
    # transaction_id/tag_id в запросе — имена колонок legacy-таблицы m2m_transaction_tags
    user_id = await get_current_user_id(token)
    time_entry = await database_worker.custom_orm_select(
        cls_from=TimeEntry,
        where_params=[
            TimeEntry.id == data.transaction_id,
            TimeEntry.user_id == user_id,
        ],
        return_unpacked=True,
    )
    if not isinstance(time_entry, TimeEntry):
        raise HTTPException(status_code=404, detail="Time entry not found")
    instance = M2M_TimeEntryLabel(
        transaction_id=data.transaction_id,
        tag_id=data.tag_id,
        relevance_score=data.relevance_score,
    )
    await database_worker.custom_insert_do_nothing(
        cls_to=M2M_TimeEntryLabel,
        index_elements=["transaction_id", "tag_id"],
        data=[instance.as_dict()],
    )
    return DefaultResponseModel(status="success", detail="Tag successfully bound to time entry")
