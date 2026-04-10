# Gateway: API тайм-менеджера

FastAPI-приложение (`main.py` → `main_app`). Точка входа для HTTP: префиксы задаются в `api/apps/__init__.py`.

## Переменные окружения

Скопируйте `example.env` в `.env` и при необходимости расширьте (email и пр. — см. `config.py`).

Обязательные для `ConfigApp`: `TIMEZONE`, `SECRET_KEY`, `ALGORITHM`, `TOKEN_EXPIRES_MINUTES`, `FRONTEND_URL`, `USERS_LIST`, плюс блок PostgreSQL для `ConfigDataBase`.

## Маршруты

### Auth — префикс `/auth`

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/auth/login` | OAuth2 form (`username` = email, `password`) → JWT |
| POST | `/auth/register` | Регистрация |
| POST | `/auth/change-password` | Смена пароля (Bearer) |
| GET | `/auth/me` | Текущий пользователь |
| GET | `/auth/users` | Список пользователей (с пагинацией) |

### Users — без дополнительного префикса

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/users` | Список (Bearer) |
| GET | `/users/{user_id}` | Карточка пользователя |
| GET | `/users/{user_id}/details` | Пользователь + проекты, задачи, напоминания, планы, записи времени с тегами |

### Time Management — без префикса (корень приложения)

Все методы ниже требуют заголовок `Authorization: Bearer <token>`.

**GET:** `/projects`, `/tasks`, `/time-entries`, `/reminders`, `/daily-plans`, `/tags`

**POST:** `/projects`, `/tasks`, `/time-entries`, `/reminders`, `/daily-plans`, `/tags`, `/time-entry-tags` (привязка тега к записи времени)

**PUT:** `/projects/{id}`, `/tasks/{id}`, `/time-entries/{id}`, `/reminders/{id}`, `/daily-plans/{id}`, `/tags/{id}`

**DELETE:** `/projects/{id}`, `/tasks/{id}`, `/time-entries/{id}`, `/reminders/{id}`, `/daily-plans/{id}`, `/tags/{id}`

## Жизненный цикл приложения

При `FORCE_RESET_DATABASE=true` в `.env` при старте выполняется сброс схемы `public` (только для разработки). Затем вызывается `alembic upgrade head` и `must_init()` — демо-данные.

## Миграции

```bash
alembic revision --autogenerate -m "описание"
alembic upgrade head
```

См. также `migrations/README.md`.

## Зависимости

`requirements.txt` / `pyproject.toml` — Python 3.13+, FastAPI, SQLAlchemy 2, asyncpg, Alembic, JWT и др.
