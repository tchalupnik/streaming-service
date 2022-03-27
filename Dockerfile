FROM python:3.8.5 as global_dependencies

RUN pip install poetry

RUN set -xe;\
    apt-get update;\
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root

COPY . /app

ENV PYTHONPATH=/app
CMD poetry run run-server
