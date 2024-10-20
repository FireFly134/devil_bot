FROM mirror.gcr.io/python:3.11.9-slim

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

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
RUN python3 -m pip install poetry
RUN poetry run pip install -U pip
RUN poetry install --no-interaction --no-ansi

COPY . .

CMD ["python3", "src/main.py"]
