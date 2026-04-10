FROM python:3.13-slim

RUN apt-get update -y && apt-get install -y ffmpeg mediainfo sox
RUN pip3 install uv

WORKDIR /src

COPY pyproject.toml .
COPY alembic.ini .

RUN uv sync

VOLUME /src
VOLUME /src/migrations

ENTRYPOINT uv run alembic upgrade head && uv run main.py