"""GET-эндпоинты префикса /auth: список пользователей и текущий пользователь."""

from fastapi import APIRouter, Depends
from fastapi.params import Query

from templates.responses import TemplatesResponsesDataclass
from templates.base_models.app_user import AppUserListResponse, AppUserModel
from core.auth.get_auth_core import (
    get_company_users_implementation,
    get_me_implementation,
)
from config import oauth2_scheme

get_auth_router = APIRouter()


@get_auth_router.get(
    "/users",
    responses={
        **TemplatesResponsesDataclass.template_404,
        **TemplatesResponsesDataclass.template_400,
        **TemplatesResponsesDataclass.template_500,
    },
    response_model=AppUserListResponse,
    description="Получение списка пользователей",
)
async def get_company_users(
    limit: int | None = Query(None, description=""),
    offset: int | None = Query(None, description=""),
    token: str = Depends(oauth2_scheme),
):
    return await get_company_users_implementation(
        limit=limit, offset=offset, token=token
    )


@get_auth_router.get(
    "/me",
    responses={
        **TemplatesResponsesDataclass.template_404,
        **TemplatesResponsesDataclass.template_400,
        **TemplatesResponsesDataclass.template_500,
    },
    response_model=AppUserModel,
    description="Получение данных текущего пользователя",
)
async def get_me_base(
    token: str = Depends(oauth2_scheme),
):
    return await get_me_implementation(token=token)
