"""Pydantic: запись времени и вложенные теги с relevance_score для ответов."""

from datetime import datetime

from pydantic import BaseModel, Field


class TimeEntryLabelModel(BaseModel):
    id: int
    name: str
    relevance_score: float


class TimeEntryCreateRequest(BaseModel):
    account_id: int
    category_id: int
    spent_minutes: float
    session_quality: float = 1.0
    note: str | None = None
    happened_at: datetime | None = None


class TimeEntryModel(BaseModel):
    id: int
    user_id: int
    account_id: int
    category_id: int
    spent_minutes: float
    session_quality: float
    note: str | None
    happened_at: datetime
    d_create: datetime


class TimeEntryListResponse(BaseModel):
    data: list[TimeEntryModel]


class TimeEntryDetailsModel(TimeEntryModel):
    tags: list[TimeEntryLabelModel] = Field(default_factory=list)
