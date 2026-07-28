#!/bin/bash

set -e -v

PORT=${PORT:-5200}
WORKERS=${WORKERS:-3}

uv run alembic upgrade head

trap "kill \$PID; wait \$PID; echo 'server stopped by SIGTERM'; exit 0" SIGINT SIGTERM
exec uv run hypercorn main:app --bind 0.0.0.0:${PORT} --workers ${WORKERS} &
PID=$!

wait $PID
