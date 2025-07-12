# syntax=docker/dockerfile:1

FROM python:3.10-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only poetry files first (to leverage caching)
COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
