"""Pydantic: проект (create/read/list)."""

from datetime import datetime

from pydantic import BaseModel


class ProjectCreateRequest(BaseModel):
    name: str
    color: str = "blue"
    priority_weight: float = 1.0


class ProjectModel(BaseModel):
    id: int
    user_id: int
    name: str
    color: str
    priority_weight: float
    is_archived: bool
    d_create: datetime


class ProjectListResponse(BaseModel):
    data: list[ProjectModel]
