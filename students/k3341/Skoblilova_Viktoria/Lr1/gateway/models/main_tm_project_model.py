"""
ORM: проект пользователя.

Таблица в БД исторически называется finance_accounts — имя сохранено для миграций.
Логически это «контейнер» задач (проект/направление работы).
"""

from sqlalchemy import Sequence, UniqueConstraint, func
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models._annotations import (
    BigintPrimaryKey,
    BoolColumn,
    DoubleColumn,
    IntegerColumn,
    TimestampColumn,
    VarcharColumn,
)
from models._base_class import Base


class Project(Base):
    """Проект: группирует задачи; принадлежит пользователю."""

    __tablename__ = "finance_accounts"
    __table_args__ = (
        UniqueConstraint("user_id", "name"),
        ForeignKeyConstraint(["user_id"], ["users.id"]),
    )

    id: Mapped[BigintPrimaryKey] = mapped_column(Sequence("finance_accounts_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    name: Mapped[VarcharColumn] = mapped_column(nullable=False)
    color: Mapped[VarcharColumn] = mapped_column(nullable=False, default="blue")
    priority_weight: Mapped[DoubleColumn] = mapped_column(nullable=False, default=1.0)
    is_archived: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)

    d_create: Mapped[TimestampColumn] = mapped_column(nullable=False, default=func.now())
