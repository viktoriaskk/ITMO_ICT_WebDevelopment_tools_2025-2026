"""Публичные (в рамках API) маршруты /users с JWT и вложенным ответом details."""

from fastapi import APIRouter, Depends, Query

from config import oauth2_scheme
from core.users.get_users_core import (
    get_user_details_implementation,
    get_user_implementation,
    get_users_implementation,
)
from templates.base_models.app_user import (
    AppUserDetailsResponse,
    AppUserListResponse,
    AppUserModel,
)

get_users_router = APIRouter()


@get_users_router.get("/users", response_model=AppUserListResponse, description="Получить список пользователей")
async def get_users(
    limit: int | None = Query(None),
    offset: int | None = Query(None),
    token: str = Depends(oauth2_scheme),
):
    return await get_users_implementation(limit=limit, offset=offset, token=token)


@get_users_router.get("/users/{user_id}", response_model=AppUserModel, description="Получить пользователя по id")
async def get_user(user_id: int, token: str = Depends(oauth2_scheme)):
    return await get_user_implementation(user_id=user_id, token=token)


@get_users_router.get("/users/{user_id}/details", response_model=AppUserDetailsResponse, description="Получить пользователя с вложенными связями")
async def get_user_details(user_id: int, token: str = Depends(oauth2_scheme)):
    return await get_user_details_implementation(user_id=user_id, token=token)
