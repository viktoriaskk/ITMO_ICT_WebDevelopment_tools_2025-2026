"""
ORM: напоминание о дедлайне задачи.

Таблица finance_budgets переиспользована под канал/момент напоминания и смещение remind_before_minutes.
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


class Reminder(Base):
    """Напоминание привязано к задаче (category_id); уникальность по (user, task, period_start)."""

    __tablename__ = "finance_budgets"
    __table_args__ = (
        UniqueConstraint("user_id", "category_id", "period_start"),
        ForeignKeyConstraint(["user_id"], ["users.id"]),
        ForeignKeyConstraint(["category_id"], ["finance_categories.id"]),
    )

    id: Mapped[BigintPrimaryKey] = mapped_column(Sequence("finance_budgets_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    category_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    period: Mapped[VarcharColumn] = mapped_column(nullable=False, default="app")
    period_start: Mapped[TimestampColumn] = mapped_column(nullable=False)
    remind_before_minutes: Mapped[DoubleColumn] = mapped_column(nullable=False, default=30.0)
    is_enabled: Mapped[BoolColumn] = mapped_column(nullable=False, default=True)

    d_create: Mapped[TimestampColumn] = mapped_column(nullable=False, default=func.now())
