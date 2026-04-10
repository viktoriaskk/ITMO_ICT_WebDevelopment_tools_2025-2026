# Лабораторная работа: бэкенд тайм-менеджера

REST API на **FastAPI** для учёта задач, дедлайнов, приоритетов, времени, напоминаний и дневных планов. Аутентификация — **JWT** (OAuth2 password flow), данные — **PostgreSQL**, миграции — **Alembic**.

## Что реализовано

- регистрация пользователя, логин (`/auth/login`), выдача JWT;
- смена пароля с проверкой текущего;
- профиль и списки пользователей: `/auth/me`, `/auth/users`, `/users`, `/users/{id}`, вложенный ответ `/users/{id}/details`;
- домен тайм-менеджера: проекты, задачи (приоритет, статус, дедлайн), записи времени, напоминания, дневные планы, теги;
- связь **многие-ко-многим** «запись времени ↔ тег» с дополнительным полем **`relevance_score`** в ассоциативной таблице;
- при старте: миграции Alembic и сиды демо-данных (`schedulers/data_init`).

Подробный отчёт для публикации на **GitHub Pages** лежит в каталоге [`/docs`](../../../../docs) репозитория (см. [корневой README](../../../../README.md)).

## Модель данных (логика ↔ физические имена таблиц)

| Сущность (ORM)   | Таблица в БД (legacy)   | Назначение |
|------------------|-------------------------|------------|
| `AppUser`        | `users`                 | Пользователь |
| `Project`        | `finance_accounts`      | Проект |
| `Task`           | `finance_categories`    | Задача |
| `TimeEntry`      | `finance_transactions`  | Запись учёта времени |
| `Label`          | `finance_tags`          | Тег |
| `M2M_TimeEntryLabel` | `m2m_transaction_tags` | M2M + `relevance_score` |
| `Reminder`       | `finance_budgets`       | Напоминание |
| `DailyPlan`      | `finance_goals`         | Дневной план |

Имена таблиц сохранены для совместимости с историей миграций Alembic.

## Структура кода (`gateway/`)

| Слой | Каталог | Роль |
|------|---------|------|
| Модели | `models/` | SQLAlchemy ORM |
| Схемы API | `templates/base_models/` | Pydantic |
| Бизнес-логика | `core/auth`, `core/time`, `core/users` | Реализации с суффиксом `*_implementation` |
| HTTP | `api/apps/` | Роутеры FastAPI |
| Миграции | `migrations/` | Alembic |

## Запуск

### Docker Compose (рекомендуется)

Из каталога `students/k3341/Skoblilova_Viktoria/Lr1`:

```bash
cp gateway/example.env gateway/.env   # при необходимости дополните переменные
docker compose up -d --build
```

API: `http://localhost:8000`. Интерактивная документация OpenAPI: `http://localhost:8000/docs` (если включена в `main.py`).

### Локально

```bash
cd gateway
pip install -r requirements.txt
# PostgreSQL и .env с POSTGRES_* должны быть доступны
alembic upgrade head
uvicorn main:main_app --host 0.0.0.0 --port 8000
```

Логин по умолчанию для демо задаётся в `schedulers/data_init.py` (пароль админа — из переменных окружения, см. `config` / `.env`).

## Полезные ссылки

- [README бэкенда](gateway/README.md) — эндпоинты и переменные окружения.
- [Отчёт для GitHub Pages](../../../../docs/index.html) — статическая страница-отчёт.
