"""POST-эндпоинты /auth: логин (OAuth2 form), регистрация, смена пароля."""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from utils.internal_workers.auth_worker import AuthNamespace
from templates.base_models.app_user import (
    AppAuthTokenResponse,
    AppChangePasswordRequest,
    DefaultResponseModel,
    RegisterRequestModel,
)
from templates.responses import TemplatesResponsesDataclass
from core.auth.post_auth_core import (
    change_password_implementation,
    register_implementation,
)
from config import oauth2_scheme

post_auth_router = APIRouter()


@post_auth_router.post(
    "/login",
    responses={
        **TemplatesResponsesDataclass.template_404,
        **TemplatesResponsesDataclass.template_400,
        **TemplatesResponsesDataclass.template_500,
    },
    response_model=AppAuthTokenResponse,
    description="Эндпоинт логина"
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await AuthNamespace.login(form_data=form_data)


@post_auth_router.post(
    "/register",
    responses={
        **TemplatesResponsesDataclass.template_404,
        **TemplatesResponsesDataclass.template_400,
        **TemplatesResponsesDataclass.template_500,
    },
    response_model=DefaultResponseModel,
    description="Эндпоинт для регистрации (mb legacy)"
)
async def register(data: RegisterRequestModel):
    return await register_implementation(data)


@post_auth_router.post(
    "/change-password",
    responses={
        **TemplatesResponsesDataclass.template_404,
        **TemplatesResponsesDataclass.template_400,
        **TemplatesResponsesDataclass.template_500,
    },
    response_model=DefaultResponseModel,
    description="Смена пароля"
)
async def change_password(
    data: AppChangePasswordRequest,
    token: str = Depends(oauth2_scheme),
):
    return await change_password_implementation(token=token, data=data)
