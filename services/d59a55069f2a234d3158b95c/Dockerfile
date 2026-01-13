# build stage
FROM python:3.10 AS builder
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install "poetry==1.8.2"
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry lock --no-update
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# final stage
FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/*
COPY . .
CMD ["uvicorn", "examples.main:app_", "--host", "0.0.0.0", "--port", "8000"]