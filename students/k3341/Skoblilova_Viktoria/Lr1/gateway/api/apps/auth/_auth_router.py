"""Объединяет GET и POST роутеры авторизации."""

from fastapi import APIRouter

from api.apps.auth.get_auth_app import get_auth_router
from api.apps.auth.post_auth_app import post_auth_router

auth_router = APIRouter()

auth_router.include_router(get_auth_router)
auth_router.include_router(post_auth_router)
