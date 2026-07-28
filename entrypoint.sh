#!/bin/bash

set -e

SERVER=${SERVER:-hypercorn}
PORT=${PORT:-5200}
WORKERS=${WORKERS:-4}

if [[ "${BUILD_DB}" != "" ]]; then
    uv alembic upgrade head
fi

trap "kill \$BGPID; wait \$BGPID; echo 'server stopped by SIGTERM'; exit 0" SIGINT SIGTERM
exec uv run ${SERVER} asgi:app --bind 0.0.0.0:${PORT} --workers ${WORKERS} &
BGPID=$!

wait $BGPID
#sleep infinity
