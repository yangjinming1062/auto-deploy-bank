# 1. Build frontend
FROM node:20-alpine as frontend
WORKDIR /app/src/frontend
COPY src/frontend/package.json src/frontend/package-lock.json* ./
RUN npm install
COPY src/frontend/ ./
RUN npm run build

# 2. Build backend
FROM python:3.10-slim as backend
WORKDIR /app
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev --extras "deploy"
COPY . .
COPY --from=frontend /app/src/frontend/build ./src/backend/langflow/frontend
RUN poetry build --format sdist && \
    cp dist/*.tar.gz /app/dist.tar.gz

# 3. Final image
FROM python:3.10-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY --from=backend /app/dist.tar.gz .
RUN pip install ./dist.tar.gz

EXPOSE 7860
CMD ["langflow", "run", "--host", "0.0.0.0", "--port", "7860", "--log-level", "info"]
