FROM mirror.gcr.io/python:3.12-slim

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    PYTHONPATH="$PYTHONPATH:/app/:/app/src/" \
    DOCKER_BUILDKIT=1

RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
        curl \
        wait-for-it \
        make \
        vim \
    && apt-get clean \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml ./pyproject.toml
COPY poetry.lock ./poetry.lock

RUN --mount=type=cache,target="$POETRY_CACHE_DIR"
RUN python3 -m pip install poetry==1.8.3
RUN poetry install --no-interaction --no-ansi

COPY . .

#CMD ["/bin/bash", "start.sh"]
