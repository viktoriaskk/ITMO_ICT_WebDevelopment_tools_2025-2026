"""ORM: пользователь приложения (аутентификация JWT, хэш пароля)."""

from sqlalchemy import Sequence, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from models._annotations import (
    BigintPrimaryKey,
    BoolColumn,
    TimestampColumn,
    Varchar1024Column,
    VarcharColumn,
)
from models._base_class import Base


class AppUser(Base):
    """Учётная запись: email уникален; пароль только в виде хэша."""

    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email"),)

    id: Mapped[BigintPrimaryKey] = mapped_column(Sequence("users_id_seq"))
    email: Mapped[VarcharColumn] = mapped_column(nullable=False)
    full_name: Mapped[VarcharColumn] = mapped_column(nullable=False)
    hashed_password: Mapped[Varchar1024Column] = mapped_column(nullable=False)
    is_active: Mapped[BoolColumn] = mapped_column(nullable=False, default=True)

    d_create: Mapped[TimestampColumn] = mapped_column(nullable=False, default=func.now())
    d_update: Mapped[TimestampColumn] = mapped_column(
        nullable=False, default=func.now(), onupdate=func.now()
    )
