"""
Настройки приложения из переменных окружения (.env).

Содержит: параметры JWT, строки подключения к PostgreSQL,
async/sync движки SQLAlchemy, OAuth2-схему для Swagger.
"""

import asyncio
import functools

from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine


def retry_async(num_attempts):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for try_index in range(num_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if try_index == num_attempts:
                        raise e
                    print(
                        f"Exception occurred: {e}. Retrying... ({try_index + 1}/{num_attempts})"
                    )
                    await asyncio.sleep(1)

        return wrapper

    return decorator


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class ConfigApp(ConfigBase):
    TIMEZONE: str
    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_EXPIRES_MINUTES: str

    FORCE_RESET_DATABASE: bool = False
    LOGLEVEL: str = "DEBUG"
    FRONTEND_URL: str
    USERS_LIST: list[int] 

class ConfigDataBase(ConfigBase):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    # REDIS_HOST: st
    # REDIS_PORT: str
    # CELERY_BROKER_URL: str
    # CELERY_RESULT_BACKEND: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def database_async_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # @property
    # def redis_url(self) -> RedisDsn | None:
    #     return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


class ConfigCall(ConfigBase):
    PROCESS_AUDIO_URL: str
    TASK_STATUS_URL: str


class ConfigSuperAdmin(ConfigBase):
    ADMIN_PASSWORD: str


class ConfigEmail(ConfigBase):
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    FROM_EMAIL: str


app_settings = ConfigApp()
db_settings = ConfigDataBase()
call_settings = ConfigCall()
admin_settings = ConfigSuperAdmin()
email_settings = ConfigEmail()


database_engine = create_engine(db_settings.database_url)
database_engine_async = create_async_engine(db_settings.database_async_url)

# oauth2_basic = OAuth2(scheme_name="Basic")
# oauth2_beaver = OAuth2(scheme_name="Beaver")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
security_company = APIKeyHeader(name="Authorization", auto_error=True)
