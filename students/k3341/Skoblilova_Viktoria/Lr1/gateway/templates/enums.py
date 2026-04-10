"""Перечисления домена: приоритет/статус задачи и канал напоминания (хранятся как строки в БД)."""

from enum import Enum


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


class ReminderChannel(str, Enum):
    APP = "app"
    EMAIL = "email"
