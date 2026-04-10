"""Pydantic: задача с приоритетом и статусом (enum → JSON)."""

from datetime import datetime

from pydantic import BaseModel

from templates.enums import TaskPriority, TaskStatus


class TaskCreateRequest(BaseModel):
    account_id: int
    name: str
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    description: str | None = None


class TaskModel(BaseModel):
    id: int
    user_id: int
    account_id: int
    name: str
    priority: TaskPriority
    status: TaskStatus
    description: str | None
    d_create: datetime


class TaskListResponse(BaseModel):
    data: list[TaskModel]
