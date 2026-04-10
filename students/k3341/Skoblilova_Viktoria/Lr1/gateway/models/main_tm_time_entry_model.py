"""
ORM: учёт времени и теги.

- TimeEntry — факт затраченного времени по задаче (таблица finance_transactions).
- Label — тег пользователя (finance_tags).
- M2M_TimeEntryLabel — связь many-to-many с полем relevance_score (ассоциативная сущность).
"""

from sqlalchemy import Sequence, UniqueConstraint, func
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models._annotations import (
    BigintPrimaryKey,
    DoubleColumn,
    IntegerColumn,
    TimestampColumn,
    Varchar1024Column,
    VarcharColumn,
)
from models._base_class import Base


class TimeEntry(Base):
    """Одна сессия/запись учёта времени: минуты, качество сессии, привязка к проекту и задаче."""

    __tablename__ = "finance_transactions"
    __table_args__ = (
        ForeignKeyConstraint(["user_id"], ["users.id"]),
        ForeignKeyConstraint(["account_id"], ["finance_accounts.id"]),
        ForeignKeyConstraint(["category_id"], ["finance_categories.id"]),
    )

    id: Mapped[BigintPrimaryKey] = mapped_column(Sequence("finance_transactions_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    account_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    category_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    spent_minutes: Mapped[DoubleColumn] = mapped_column(nullable=False, default=0.0)
    session_quality: Mapped[DoubleColumn] = mapped_column(nullable=False, default=1.0)
    note: Mapped[Varchar1024Column] = mapped_column(nullable=True)
    happened_at: Mapped[TimestampColumn] = mapped_column(nullable=False, default=func.now())
    d_create: Mapped[TimestampColumn] = mapped_column(nullable=False, default=func.now())


class Label(Base):
    """Метка (тег) для классификации записей времени."""

    __tablename__ = "finance_tags"
    __table_args__ = (
        UniqueConstraint("user_id", "name"),
        ForeignKeyConstraint(["user_id"], ["users.id"]),
    )

    id: Mapped[BigintPrimaryKey] = mapped_column(Sequence("finance_tags_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    name: Mapped[VarcharColumn] = mapped_column(nullable=False)


class M2M_TimeEntryLabel(Base):
    """Связь запись времени ↔ тег; relevance_score — сила/релевантность привязки."""

    __tablename__ = "m2m_transaction_tags"
    __table_args__ = (
        UniqueConstraint("transaction_id", "tag_id"),
        ForeignKeyConstraint(["transaction_id"], ["finance_transactions.id"]),
        ForeignKeyConstraint(["tag_id"], ["finance_tags.id"]),
    )

    transaction_id: Mapped[IntegerColumn] = mapped_column(primary_key=True)
    tag_id: Mapped[IntegerColumn] = mapped_column(primary_key=True)
    relevance_score: Mapped[DoubleColumn] = mapped_column(nullable=False, default=1.0)
