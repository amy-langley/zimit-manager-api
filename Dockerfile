FROM python:3.12-alpine AS base

RUN apk add curl \
    && curl -sSL https://pdm-project.org/install-pdm.py | python3 -

WORKDIR /app

ENV PATH="/root/.local/bin:$PATH"
ENV SQLITE_FILENAME=/data/database.db
ENV DEFAULT_OUTPUT_DIR=/Users/amy/work/zimit-manager/var/output

COPY pyproject.toml pdm.lock /app/

RUN pdm install --prod

COPY src /app/src
COPY scripts /app/scripts

RUN pdm install --prod

EXPOSE 8000

ENTRYPOINT ["/app/scripts/run_server.sh"]
