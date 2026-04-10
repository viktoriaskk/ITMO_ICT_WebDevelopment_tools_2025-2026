"""Pydantic: напоминание о задаче (канал + момент period_start)."""

from datetime import datetime

from pydantic import BaseModel

from templates.enums import ReminderChannel


class ReminderCreateRequest(BaseModel):
    category_id: int
    period: ReminderChannel = ReminderChannel.APP
    period_start: datetime
    remind_before_minutes: float = 30.0
    is_enabled: bool = True


class ReminderModel(BaseModel):
    id: int
    user_id: int
    category_id: int
    period: ReminderChannel
    period_start: datetime
    remind_before_minutes: float
    is_enabled: bool
    d_create: datetime


class ReminderListResponse(BaseModel):
    data: list[ReminderModel]
