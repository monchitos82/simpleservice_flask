# build the project
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv

WORKDIR /simpleservice
RUN python -m venv $VIRTUAL_ENV
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN /opt/venv/bin/pip install --upgrade pip && /opt/venv/bin/pip install -r requirements.txt

# run the project
ARG BUILD_DB
COPY . .

WORKDIR /simpleservice
CMD ["/simpleservice/entrypoint.sh"]