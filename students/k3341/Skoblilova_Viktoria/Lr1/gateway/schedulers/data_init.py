"""
Инициализация данных после миграций: админ-пользователь и демо-сущности тайм-менеджера.

Вызывается из main.lifespan после `alembic upgrade head`.
Имена функций init_default_* частично исторические (categories/account) — по смыслу это задачи/проект.
"""

import logging
from datetime import datetime, timezone

from config import admin_settings, database_engine_async
from models.main_app_user_model import AppUser
from models.main_tm_daily_plan_model import DailyPlan
from models.main_tm_project_model import Project
from models.main_tm_reminder_model import Reminder
from models.main_tm_task_model import Task
from models.main_tm_time_entry_model import Label, M2M_TimeEntryLabel, TimeEntry
from utils.internal_workers.auth_worker import AuthNamespace
from utils.internal_workers.database_worker import DatabaseWorkerAsync

database_worker = DatabaseWorkerAsync(database_engine_async)
logger = logging.getLogger("app.schedulers.data_init")


async def init_default_user():
    """Создаёт или обновляет администратора по email из настроек."""
    hashed_password = AuthNamespace._get_password_hash(admin_settings.ADMIN_PASSWORD)
    user = await database_worker.custom_upsert(
        cls_to=AppUser,
        index_elements=["email"],
        data=[
            AppUser(
                email="admin@example.com",
                full_name="Admin",
                hashed_password=hashed_password,
            ).as_dict()
        ],
        update_set=["full_name", "hashed_password", "is_active"],
        returning=AppUser,
        return_unpacked=True,
    )
    return user


async def init_default_categories(user_id: int):
    """Демо-задачи внутри проекта «Учеба» (создаёт проект при отсутствии)."""
    project = await database_worker.custom_orm_select(
        cls_from=Project,
        where_params=[Project.user_id == user_id, Project.name == "Учеба"],
        return_unpacked=True,
    )
    if not project:
        project = await init_default_account(user_id)

    tasks = [
        {
            "name": "Подготовка к практике",
            "priority": "high",
            "status": "in_progress",
            "description": "Проработка ORM и миграций",
        },
        {
            "name": "Реализация CRUD",
            "priority": "critical",
            "status": "todo",
            "description": "Ручки FastAPI + проверки",
        },
    ]
    for item in tasks:
        await database_worker.custom_upsert(
            cls_to=Task,
            index_elements=["user_id", "name", "account_id"],
            data=[Task(user_id=user_id, account_id=project.id, **item).as_dict()],
            update_set=["priority", "status", "description"],
        )


async def init_default_account(user_id: int):
    """Демо-проект «Учеба» для привязки задач."""
    return await database_worker.custom_upsert(
        cls_to=Project,
        index_elements=["user_id", "name"],
        data=[
            Project(
                user_id=user_id,
                name="Учеба",
                color="purple",
                priority_weight=1.0,
                is_archived=False,
            ).as_dict()
        ],
        update_set=["color", "priority_weight", "is_archived"],
        returning=Project,
        return_unpacked=True,
    )


async def init_default_budget(user_id: int):
    """Пример напоминания для задачи «Реализация CRUD»."""
    task = await database_worker.custom_orm_select(
        cls_from=Task,
        where_params=[Task.user_id == user_id, Task.name == "Реализация CRUD"],
        return_unpacked=True,
    )
    if not task:
        return
    await database_worker.custom_upsert(
        cls_to=Reminder,
        index_elements=["user_id", "category_id", "period_start"],
        data=[
            Reminder(
                user_id=user_id,
                category_id=task.id,
                period="app",
                period_start=datetime.now(timezone.utc),
                remind_before_minutes=60.0,
                is_enabled=True,
            ).as_dict()
        ],
        update_set=["period", "remind_before_minutes", "is_enabled"],
    )


async def init_default_goal(user_id: int):
    """Пример дневного плана на текущую дату."""
    await database_worker.custom_upsert(
        cls_to=DailyPlan,
        index_elements=["user_id", "name"],
        data=[
            DailyPlan(
                user_id=user_id,
                name="План на сегодня",
                date_for=datetime.now(timezone.utc),
                planned_minutes=240,
                notes="2 блока глубокой работы",
                status="todo",
                is_generated=False,
            ).as_dict()
        ],
        update_set=["date_for", "planned_minutes", "notes", "status", "is_generated"],
    )


async def init_default_tags(user_id: int):
    """Набор тегов по умолчанию для демонстрации many-to-many."""
    for tag_name in ["important", "recurring", "planned"]:
        await database_worker.custom_upsert(
            cls_to=Label,
            index_elements=["user_id", "name"],
            data=[Label(user_id=user_id, name=tag_name).as_dict()],
            update_set=["name"],
        )


async def init_default_transaction(user_id: int, account_id: int):
    """Демо-запись времени и связь с тегом important (если ещё нет)."""
    task = await database_worker.custom_orm_select(
        cls_from=Task,
        where_params=[Task.user_id == user_id, Task.name == "Подготовка к практике"],
        return_unpacked=True,
    )
    if not task:
        return

    rows = await database_worker.custom_orm_select(
        cls_from=TimeEntry,
        where_params=[
            TimeEntry.user_id == user_id,
            TimeEntry.account_id == account_id,
            TimeEntry.category_id == task.id,
            TimeEntry.spent_minutes == 120.0,
        ],
        order_by=[TimeEntry.id.asc()],
        sql_limit=1,
    )
    transaction = rows[0] if rows else None
    if not transaction:
        inserted = await database_worker.custom_insert(
            cls_to=TimeEntry,
            data=[
                TimeEntry(
                    user_id=user_id,
                    account_id=account_id,
                    category_id=task.id,
                    spent_minutes=120.0,
                    session_quality=0.9,
                    note="Первый рабочий блок",
                ).as_dict()
            ],
            returning=TimeEntry,
        )
        transaction = inserted[0] if isinstance(inserted, list) and inserted else None

    default_tag = await database_worker.custom_orm_select(
        cls_from=Label,
        where_params=[Label.user_id == user_id, Label.name == "important"],
        return_unpacked=True,
    )
    if transaction and default_tag:
        await database_worker.custom_insert_do_nothing(
            cls_to=M2M_TimeEntryLabel,
            index_elements=["transaction_id", "tag_id"],
            data=[
                M2M_TimeEntryLabel(
                    transaction_id=transaction.id,
                    tag_id=default_tag.id,
                    relevance_score=1.0,
                ).as_dict()
            ],
        )


async def must_init(app=None):
    """Точка входа: последовательно вызывает все init_default_*."""
    try:
        user = await init_default_user()
        await init_default_categories(user.id)
        account = await init_default_account(user.id)
        await init_default_budget(user.id)
        await init_default_goal(user.id)
        await init_default_tags(user.id)
        await init_default_transaction(user.id, account.id)
        logger.info("Default time management data initialized")
    except Exception as exception:
        logger.error(f"Failed to initialize default time management data: {exception}")
