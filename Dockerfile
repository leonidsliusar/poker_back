FROM python:3.11-slim-buster

EXPOSE 8000

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VERSION=1.8

RUN pip install -U "poetry==$POETRY_VERSION" && poetry config virtualenvs.create false

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml ./
COPY ./src ./src

RUN poetry install --no-cache --no-ansi --without test
CMD ["poetry", "run", "server"]