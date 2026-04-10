"""
Эндпоинты /auth (POST): регистрация, смена пароля.

Регистрация создаёт запись AppUser; смена пароля пересчитывает хэш через AuthNamespace.
"""

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from config import database_engine_async
from logs.log_worker import custom_core_decorator
from models.main_app_user_model import AppUser
from templates.base_models.app_user import (
    AppChangePasswordRequest,
    DefaultResponseModel,
    RegisterRequestModel,
)
from utils.internal_workers.auth_worker import AuthNamespace
from utils.internal_workers.database_worker import DatabaseWorkerAsync


database_worker = DatabaseWorkerAsync(database_engine_async)


@custom_core_decorator
async def register_implementation(data: RegisterRequestModel):
    exists = await database_worker.custom_orm_select(
        cls_from=AppUser, where_params=[AppUser.email == data.email]
    )
    if isinstance(exists, list) and exists:
        raise HTTPException(status_code=400, detail="Email already exists")

    user_instance = AppUser(
        email=data.email,
        full_name=data.full_name,
        hashed_password=AuthNamespace._get_password_hash(data.password),
    )
    try:
        await database_worker.custom_insert(
            cls_to=AppUser, data=[user_instance.as_dict()], returning=AppUser
        )
    except IntegrityError as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    return DefaultResponseModel(status="success", detail="User successfully created")


@custom_core_decorator
async def change_password_implementation(
    token: str, data: AppChangePasswordRequest
):
    user: AppUser = await AuthNamespace.get_current_user(token=token)
    if not AuthNamespace._verify_password(data.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is invalid")
    await database_worker.custom_update(
        cls_to=AppUser,
        where_params=[AppUser.id == user.id],
        data={"hashed_password": AuthNamespace._get_password_hash(data.new_password)},
    )
    return DefaultResponseModel(
        status="success", detail="Password successfully changed"
    )
