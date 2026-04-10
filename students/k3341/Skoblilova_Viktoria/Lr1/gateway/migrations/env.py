"""
Конфигурация Alembic: offline/online миграции против PostgreSQL.

target_metadata строится из DeclarativeBase всех ORM-моделей, импортируемых через models._base_class.
"""

from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy import create_engine
from alembic import context
from config import db_settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from models._base_class import Base

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = f"postgresql+psycopg2://{db_settings.POSTGRES_USER}:{db_settings.POSTGRES_PASSWORD}@{db_settings.POSTGRES_HOST}:{db_settings.POSTGRES_PORT}/{db_settings.POSTGRES_DB}"
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(
        f"postgresql+psycopg2://{db_settings.POSTGRES_USER}:{db_settings.POSTGRES_PASSWORD}"
        f"@{db_settings.POSTGRES_HOST}:{db_settings.POSTGRES_PORT}/{db_settings.POSTGRES_DB}",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
