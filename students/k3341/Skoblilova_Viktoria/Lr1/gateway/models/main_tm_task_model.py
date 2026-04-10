"""
ORM: задача с приоритетом, статусом и сроком/описанием.

Таблица: finance_categories; account_id — связь с проектом (finance_accounts).
"""

from sqlalchemy import Sequence, UniqueConstraint, func
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models._annotations import (
    BigintPrimaryKey,
    IntegerColumn,
    TimestampColumn,
    VarcharColumn,
)
from models._base_class import Base


class Task(Base):
    """Задача внутри проекта; priority/status хранятся строками (см. enums в Pydantic)."""

    __tablename__ = "finance_categories"
    __table_args__ = (
        UniqueConstraint("user_id", "name", "account_id"),
        ForeignKeyConstraint(["user_id"], ["users.id"]),
        ForeignKeyConstraint(["account_id"], ["finance_accounts.id"]),
    )

    id: Mapped[BigintPrimaryKey] = mapped_column(Sequence("finance_categories_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    account_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    name: Mapped[VarcharColumn] = mapped_column(nullable=False)
    priority: Mapped[VarcharColumn] = mapped_column(nullable=False, default="medium")
    status: Mapped[VarcharColumn] = mapped_column(nullable=False, default="todo")
    description: Mapped[VarcharColumn] = mapped_column(nullable=True)

    d_create: Mapped[TimestampColumn] = mapped_column(nullable=False, default=func.now())
