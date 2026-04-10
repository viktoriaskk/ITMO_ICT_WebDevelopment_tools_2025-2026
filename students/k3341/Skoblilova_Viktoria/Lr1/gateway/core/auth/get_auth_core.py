"""
Эндпоинты раздела /auth (GET): список пользователей и профиль «я».

Требуют валидный JWT; список доступен любому аутентифицированному пользователю (как в шаблоне).
"""

from models.main_app_user_model import AppUser
from templates.base_models.app_user import AppUserListResponse, AppUserModel
from logs.log_worker import custom_core_decorator
from utils.internal_workers.auth_worker import AuthNamespace
from utils.internal_workers.database_worker import DatabaseWorkerAsync
from config import database_engine_async

database_worker = DatabaseWorkerAsync(database_engine_async)


@custom_core_decorator
async def get_company_users_implementation(
    limit: int,
    offset: int,
    token: str,
):
    await AuthNamespace.get_current_user(token=token)
    users = await database_worker.custom_orm_select(
        cls_from=AppUser,
        sql_limit=limit,
        offset=offset,
        order_by=[AppUser.id.asc()],
    )
    total_count = await database_worker.count(cls_from=AppUser)
    return AppUserListResponse(
        total_count=total_count[0],
        users=[
            AppUserModel(
                id=row.id,
                email=row.email,
                full_name=row.full_name,
                is_active=row.is_active,
                d_create=row.d_create,
            )
            for row in users
        ],
    )


@custom_core_decorator
async def get_me_implementation(token: str):
    user: AppUser = await AuthNamespace.get_current_user(token=token)
    return AppUserModel(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        d_create=user.d_create,
    )
