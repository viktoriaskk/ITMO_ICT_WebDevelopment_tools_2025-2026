"""
Точка входа FastAPI-приложения тайм-менеджера.

При старте: опциональный сброс схемы БД, применение миграций Alembic,
затем инициализация демо-данных (см. schedulers.data_init).
"""

import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from scalar_fastapi import Theme
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import text

from api import api_router
from config import app_settings, database_engine_async
from middlewares.permission import PermissionMiddleware
from schedulers.data_init import must_init

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logging.getLogger("httpx").setLevel(logging.WARNING)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл приложения: миграции и сиды до приёма запросов."""
    try:
        # Полный сброс public-схемы (только если явно включено в настройках)
        if app_settings.FORCE_RESET_DATABASE:
            async with database_engine_async.begin() as conn:
                await conn.execute(text(f"DROP SCHEMA public CASCADE;"))
                await conn.execute(text(f"CREATE SCHEMA public;"))
            logging.info("Database has been reset to base state")

        # Синхронный процесс alembic: схема БД должна совпадать с ORM-моделями
        proc = await asyncio.create_subprocess_exec(
            "alembic",
            "upgrade",
            "head",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            logging.error(f"Alembic migration failed. ({stderr.decode()})")
            raise RuntimeError(f"Migration error: ({stderr.decode()})")

        logging.info(f"Database migrations applied successfully. ({stdout.decode()})")
        # Демо-пользователь и примеры сущностей для быстрой проверки API
        await must_init()

        yield
    finally:
        pass


main_app = FastAPI(
    title="Template API",
    description="...",
    version="0.1.0",
    lifespan=lifespan,
)





main_app.include_router(api_router)


main_app.add_middleware(
    PermissionMiddleware,
)
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
