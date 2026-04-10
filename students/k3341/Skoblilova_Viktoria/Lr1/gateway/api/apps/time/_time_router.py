"""Сборка подроутеров GET/POST/PUT/DELETE для домена тайм-менеджера."""

from fastapi import APIRouter

from api.apps.time.delete_time_app import delete_time_router
from api.apps.time.get_time_app import get_time_router
from api.apps.time.post_time_app import post_time_router
from api.apps.time.put_time_app import put_time_router

time_router = APIRouter()
time_router.include_router(get_time_router)
time_router.include_router(post_time_router)
time_router.include_router(put_time_router)
time_router.include_router(delete_time_router)
