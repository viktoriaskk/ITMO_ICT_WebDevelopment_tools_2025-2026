# web

Репозиторий с лабораторной работой: **бэкенд тайм-менеджера** на FastAPI.

## Содержимое

| Каталог | Описание |
|---------|----------|
| [`students/k3341/Skoblilova_Viktoria/Lr1/`](students/k3341/Skoblilova_Viktoria/Lr1/) | Docker Compose, сервис `gateway`, PostgreSQL |
| [`students/k3341/Skoblilova_Viktoria/Lr1/gateway/`](students/k3341/Skoblilova_Viktoria/Lr1/gateway/) | Исходный код API |
| [`docs/`](docs/) | Статический **отчёт** для публикации на GitHub Pages |

## Документация

- [README лабораторной](students/k3341/Skoblilova_Viktoria/Lr1/README.md) — цели, модель данных, запуск.
- [README gateway](students/k3341/Skoblilova_Viktoria/Lr1/gateway/README.md) — таблица эндпоинтов и окружение.

## GitHub Pages: как опубликовать отчёт

1. В репозитории на GitHub: **Settings** → **Pages**.
2. В разделе **Build and deployment**: Source — **Deploy from a branch**.
3. Branch — `main` (или ваша основная ветка), folder — **`/docs`**, Save.

Через минуту сайт будет доступен по адресу вида `https://<user>.github.io/<repo>/` — откроется [`docs/index.html`](docs/index.html).

Файл [`docs/.nojekyll`](docs/.nojekyll) отключает обработку Jekyll, чтобы GitHub Pages отдавал страницу как есть.
