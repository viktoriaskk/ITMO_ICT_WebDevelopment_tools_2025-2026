"""Pydantic: дневной план работы на дату date_for."""

from datetime import datetime

from pydantic import BaseModel

from templates.enums import TaskStatus


class DailyPlanCreateRequest(BaseModel):
    name: str
    date_for: datetime
    planned_minutes: int
    notes: str | None = None
    status: TaskStatus = TaskStatus.TODO
    is_generated: bool = False


class DailyPlanModel(BaseModel):
    id: int
    user_id: int
    name: str
    date_for: datetime
    planned_minutes: int
    notes: str | None
    status: TaskStatus
    is_generated: bool
    d_create: datetime


class DailyPlanListResponse(BaseModel):
    data: list[DailyPlanModel]
