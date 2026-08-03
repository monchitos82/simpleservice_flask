# build the project
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd simpleservice
RUN useradd simpleservice -g simpleservice -m -d /opt/simpleservice

USER simpleservice
WORKDIR /opt/simpleservice

COPY --chown=simpleservice:simpleservice . .

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/opt/simpleservice/.local/bin:$PATH"

RUN uv sync --frozen

CMD ["/opt/simpleservice/entrypoint.sh"]
