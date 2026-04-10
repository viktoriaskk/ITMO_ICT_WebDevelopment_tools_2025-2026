"""Pydantic: тег и тело запроса привязки к записи времени (id полей — legacy имён колонок)."""

from pydantic import BaseModel


class LabelModel(BaseModel):
    id: int
    user_id: int
    name: str


class LabelCreateRequest(BaseModel):
    name: str


class LabelListResponse(BaseModel):
    data: list[LabelModel]


class TimeEntryLabelBindRequest(BaseModel):
    transaction_id: int
    tag_id: int
    relevance_score: float = 1.0
