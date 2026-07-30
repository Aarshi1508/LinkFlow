#!/bin/sh
# Runs on every container start. Running migrations here (rather than as a
# separate manual step) means the DB schema is always in sync with the code
# that's about to run, without a human needing to remember to do it.
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
