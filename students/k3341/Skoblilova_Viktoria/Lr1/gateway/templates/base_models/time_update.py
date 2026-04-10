"""Pydantic: частичные обновления (PATCH-семантика через exclude_unset в core)."""

from datetime import datetime

from pydantic import BaseModel

from templates.enums import ReminderChannel, TaskPriority, TaskStatus


class ProjectUpdateRequest(BaseModel):
    name: str | None = None
    color: str | None = None
    priority_weight: float | None = None
    is_archived: bool | None = None


class TaskUpdateRequest(BaseModel):
    name: str | None = None
    account_id: int | None = None
    priority: TaskPriority | None = None
    status: TaskStatus | None = None
    description: str | None = None


class TimeEntryUpdateRequest(BaseModel):
    account_id: int | None = None
    category_id: int | None = None
    spent_minutes: float | None = None
    session_quality: float | None = None
    note: str | None = None
    happened_at: datetime | None = None


class ReminderUpdateRequest(BaseModel):
    category_id: int | None = None
    period: ReminderChannel | None = None
    period_start: datetime | None = None
    remind_before_minutes: float | None = None
    is_enabled: bool | None = None


class DailyPlanUpdateRequest(BaseModel):
    name: str | None = None
    date_for: datetime | None = None
    planned_minutes: int | None = None
    notes: str | None = None
    status: TaskStatus | None = None
    is_generated: bool | None = None


class LabelUpdateRequest(BaseModel):
    name: str | None = None
