"""
Типовые аннотации колонок PostgreSQL для Mapped[mapped_column].

Упрощают объявление полей в моделях и единообразие типов в БД.
"""

import datetime
from typing import Annotated

from sqlalchemy.dialects.postgresql import (
    ARRAY,
    BIGINT,
    BOOLEAN,
    DATE,
    DOUBLE_PRECISION,
    INTEGER,
    JSONB,
    NUMERIC,
    SMALLINT,
    TEXT,
    TIMESTAMP,
    VARCHAR,
)
from sqlalchemy.orm import mapped_column


IntegerPrimaryKey = Annotated[
    int,
    mapped_column(
        INTEGER,
        primary_key=True,
        nullable=False,
        index=True,
    ),
]

BigintPrimaryKey = Annotated[
    int,
    mapped_column(
        BIGINT,
        primary_key=True,
        nullable=False,
        index=True,
    ),
]

TextPrimaryKey = Annotated[
    str,
    mapped_column(
        TEXT,
        primary_key=True,
        nullable=False,
        index=True,
    ),
]

BigintColumn = Annotated[
    int,
    mapped_column(BIGINT, nullable=True),
]

SmallintColumn = Annotated[
    int,
    mapped_column(SMALLINT),
]

IntegerColumn = Annotated[
    int,
    mapped_column(INTEGER),
]

TextColumn = Annotated[
    str,
    mapped_column(TEXT, nullable=True),
]

BoolColumn = Annotated[
    bool,
    mapped_column(BOOLEAN, nullable=True),
]

DoubleColumn = Annotated[
    float,
    mapped_column(DOUBLE_PRECISION),
]

NumericColumn = Annotated[
    int,
    mapped_column(NUMERIC),
]

VarcharColumn = Annotated[
    str,
    mapped_column(VARCHAR),
]

TimestampColumn = Annotated[
    datetime.datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
    ),
]

TimestampWTColumn = Annotated[
    datetime.datetime,
    mapped_column(
        TIMESTAMP(timezone=False),
    ),
]

DateColumn = Annotated[
    datetime.datetime,
    mapped_column(DATE),
]

JsonbColumn = Annotated[dict, mapped_column(JSONB)]

ListIntegerColumn = Annotated[
    list[int],
    mapped_column(ARRAY(INTEGER)),
]

ListNumericColumn = Annotated[
    list[float],
    mapped_column(ARRAY(NUMERIC)),
]

ListTextColumn = Annotated[
    list[str],
    mapped_column(ARRAY(TEXT)),
]

ListSmallintColumn = Annotated[
    list[int],
    mapped_column(SMALLINT),
]

ListJsonbColumn = Annotated[list[dict], mapped_column(ARRAY(JSONB))]

Varchar1024Column = Annotated[
    str,
    mapped_column(VARCHAR(1024)),
]

Varchar2048Column = Annotated[
    str,
    mapped_column(VARCHAR(2048)),
]
