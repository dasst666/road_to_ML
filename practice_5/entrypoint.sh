#!/usr/bin/env bash
set -euo pipefail

echo "Waiting for Postgres at ${DB_HOST:-db}:${DB_PORT:-5432}..."
for i in {1..40}; do
  if pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${POSTGRES_USER:-postgres}" >/dev/null 2>&1; then
    echo "Postgres is ready ✅"
    break
  fi
  echo "Postgres not ready yet... ($i)"
  sleep 2
done

echo "Running alembic upgrade head..."
alembic upgrade head

echo "Starting Uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000