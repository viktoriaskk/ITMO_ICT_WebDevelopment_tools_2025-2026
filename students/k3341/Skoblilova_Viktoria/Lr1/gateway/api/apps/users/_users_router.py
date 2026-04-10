"""Роутер раздела пользователей."""

from fastapi import APIRouter

from api.apps.users.get_users_app import get_users_router

users_router = APIRouter()
users_router.include_router(get_users_router)
