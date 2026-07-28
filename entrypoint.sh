#!/bin/bash

set -e

SERVER=${SERVER:-hypercorn}
PORT=${PORT:-5200}
WORKERS=${WORKERS:-4}

if [[ "${BUILD_DB}" == "yes" ]]; then
    uv alembic upgrade head
fi

uv run ${SERVER} asgi:app --bind 0.0.0.0:${PORT} --workers ${WORKERS} &

sleep infinity