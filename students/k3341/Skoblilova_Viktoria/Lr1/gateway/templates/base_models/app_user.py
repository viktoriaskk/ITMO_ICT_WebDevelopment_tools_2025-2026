"""
Схемы пользователя и авторизации: регистрация, JWT, смена пароля, вложенный профиль.

AppUserDetailsResponse агрегирует сущности тайм-менеджера для GET .../details.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr

from templates.base_models.time_daily_plan import DailyPlanModel
from templates.base_models.time_entry import TimeEntryDetailsModel
from templates.base_models.time_project import ProjectModel
from templates.base_models.time_reminder import ReminderModel
from templates.base_models.time_task import TaskModel


class AppUserCreateRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class RegisterRequestModel(AppUserCreateRequest):
    pass


class AppLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AppChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class AppAuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DefaultResponseModel(BaseModel):
    status: str
    detail: str


class AppUserModel(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    d_create: datetime


class AppUserListResponse(BaseModel):
    total_count: int
    users: list[AppUserModel]


class AppUserDetailsResponse(BaseModel):
    user: AppUserModel
    projects: list[ProjectModel]
    tasks: list[TaskModel]
    reminders: list[ReminderModel]
    daily_plans: list[DailyPlanModel]
    time_entries: list[TimeEntryDetailsModel]
