"""
ORM: дневной план (расписание на дату).

Таблица finance_goals: запланированные блоки времени и статус выполнения.
"""

from sqlalchemy import Sequence, UniqueConstraint, func
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models._annotations import (
    BigintPrimaryKey,
    BoolColumn,
    IntegerColumn,
    TimestampColumn,
    VarcharColumn,
)
from models._base_class import Base


class DailyPlan(Base):
    """План на конкретный день: имя, дата, запланированные минуты, заметки."""

    __tablename__ = "finance_goals"
    __table_args__ = (
        UniqueConstraint("user_id", "name"),
        ForeignKeyConstraint(["user_id"], ["users.id"]),
    )

    id: Mapped[BigintPrimaryKey] = mapped_column(Sequence("finance_goals_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    name: Mapped[VarcharColumn] = mapped_column(nullable=False)
    date_for: Mapped[TimestampColumn] = mapped_column(nullable=False)
    planned_minutes: Mapped[IntegerColumn] = mapped_column(nullable=False, default=0)
    notes: Mapped[VarcharColumn] = mapped_column(nullable=True)
    status: Mapped[VarcharColumn] = mapped_column(nullable=False, default="todo")
    is_generated: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)

    d_create: Mapped[TimestampColumn] = mapped_column(nullable=False, default=func.now())
