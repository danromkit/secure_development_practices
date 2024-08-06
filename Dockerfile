FROM python:3.12-slim-bookworm as poetry
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.8.3

RUN pip install "poetry==$POETRY_VERSION"

FROM poetry as app
WORKDIR app
COPY pyproject.toml pyproject.toml
RUN poetry install
COPY . .
CMD poetry run python3 main.py
