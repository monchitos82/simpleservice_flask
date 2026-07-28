#!/bin/bash

PORT=${PORT}
if [[ "${PORT}" = "" ]]; then
  PORT=5200
fi

WORKERS=${WORKERS}
if [[ "${WORKERS}" = "" ]]; then
  WORKERS=4
fi

BUILD_DB=${BUILD_DB}
if [[ "${BUILD_DB}" == "yes" ]]; then
    /opt/venv/bin alembic upgrade head
fi

/opt/venv/bin/hypercorn asgi:app --bind 0.0.0.0:${PORT} --workers ${WORKERS} &
sleep infinity