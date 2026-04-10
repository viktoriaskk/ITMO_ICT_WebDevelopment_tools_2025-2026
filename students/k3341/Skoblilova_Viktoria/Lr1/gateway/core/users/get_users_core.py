"""
Пользователи: список, карточка и «детали» с вложенными сущностями тайм-менеджера.

Детальный ответ собирает проекты, задачи, напоминания, планы и записи времени;
для записей времени подгружаются теги через M2M_TimeEntryLabel.
"""

from config import database_engine_async
from fastapi import HTTPException
from models.main_app_user_model import AppUser
from models.main_tm_daily_plan_model import DailyPlan
from models.main_tm_project_model import Project
from models.main_tm_reminder_model import Reminder
from models.main_tm_task_model import Task
from models.main_tm_time_entry_model import Label, M2M_TimeEntryLabel, TimeEntry
from templates.base_models.app_user import (
    AppUserDetailsResponse,
    AppUserListResponse,
    AppUserModel,
)
from templates.base_models.time_daily_plan import DailyPlanModel
from templates.base_models.time_entry import TimeEntryDetailsModel, TimeEntryLabelModel
from templates.base_models.time_project import ProjectModel
from templates.base_models.time_reminder import ReminderModel
from templates.base_models.time_task import TaskModel
from logs.log_worker import custom_core_decorator
from utils.internal_workers.auth_worker import AuthNamespace
from utils.internal_workers.database_worker import DatabaseWorkerAsync

database_worker = DatabaseWorkerAsync(database_engine_async)


@custom_core_decorator
async def get_users_implementation(limit: int | None, offset: int | None, token: str):
    await AuthNamespace.get_current_user(token=token)
    users = await database_worker.custom_orm_select(
        cls_from=AppUser, sql_limit=limit, offset=offset, order_by=[AppUser.id.asc()]
    )
    total_count = await database_worker.count(cls_from=AppUser)
    return AppUserListResponse(
        total_count=total_count[0],
        users=[AppUserModel(**u.as_dict()) for u in users],
    )


@custom_core_decorator
async def get_user_implementation(user_id: int, token: str):
    await AuthNamespace.get_current_user(token=token)
    user = await database_worker.custom_orm_select(
        cls_from=AppUser, where_params=[AppUser.id == user_id], return_unpacked=True
    )
    if not isinstance(user, AppUser):
        raise HTTPException(status_code=404, detail="User not found")
    return AppUserModel(**user.as_dict())


@custom_core_decorator
async def get_user_details_implementation(user_id: int, token: str):
    await AuthNamespace.get_current_user(token=token)
    user = await database_worker.custom_orm_select(
        cls_from=AppUser, where_params=[AppUser.id == user_id], return_unpacked=True
    )
    if not isinstance(user, AppUser):
        raise HTTPException(status_code=404, detail="User not found")

    projects = await database_worker.custom_orm_select(
        cls_from=Project,
        where_params=[Project.user_id == user_id],
        order_by=[Project.id.asc()],
    )
    tasks = await database_worker.custom_orm_select(
        cls_from=Task,
        where_params=[Task.user_id == user_id],
        order_by=[Task.id.asc()],
    )
    reminders = await database_worker.custom_orm_select(
        cls_from=Reminder,
        where_params=[Reminder.user_id == user_id],
        order_by=[Reminder.id.asc()],
    )
    daily_plans = await database_worker.custom_orm_select(
        cls_from=DailyPlan,
        where_params=[DailyPlan.user_id == user_id],
        order_by=[DailyPlan.id.asc()],
    )
    time_entries = await database_worker.custom_orm_select(
        cls_from=TimeEntry,
        where_params=[TimeEntry.user_id == user_id],
        order_by=[TimeEntry.id.asc()],
    )

    # Для каждой записи времени подтягиваем связанные теги одним запросом (many-to-many)
    entry_ids = [entry.id for entry in time_entries]
    tag_rows = []
    if entry_ids:
        tag_rows = await database_worker.custom_orm_select(
            cls_from=[
                M2M_TimeEntryLabel.transaction_id,
                Label.id,
                Label.name,
                M2M_TimeEntryLabel.relevance_score,
            ],
            select_from=[M2M_TimeEntryLabel],
            join_on=[(Label, Label.id == M2M_TimeEntryLabel.tag_id)],
            where_params=[M2M_TimeEntryLabel.transaction_id.in_(entry_ids)],
        )

    labels_by_entry = {}
    for row in tag_rows:
        labels_by_entry.setdefault(row[0], []).append(
            TimeEntryLabelModel(id=row[1], name=row[2], relevance_score=float(row[3]))
        )

    time_entry_payload = []
    for time_entry in time_entries:
        time_entry_payload.append(
            TimeEntryDetailsModel(
                **time_entry.as_dict(), tags=labels_by_entry.get(time_entry.id, [])
            )
        )

    return AppUserDetailsResponse(
        user=AppUserModel(**user.as_dict()),
        projects=[ProjectModel(**project.as_dict()) for project in projects],
        tasks=[TaskModel(**task.as_dict()) for task in tasks],
        reminders=[ReminderModel(**reminder.as_dict()) for reminder in reminders],
        daily_plans=[DailyPlanModel(**daily_plan.as_dict()) for daily_plan in daily_plans],
        time_entries=time_entry_payload,
    )
