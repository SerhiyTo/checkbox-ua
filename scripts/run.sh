#!/bin/bash
poetry run alembic upgrade head
poetry run uvicorn src.main:app --host 0.0.0.0 --port ${APP_PORT} --workers 4 --backlog 2048 --timeout-keep-alive 5 --limit-concurrency 100
