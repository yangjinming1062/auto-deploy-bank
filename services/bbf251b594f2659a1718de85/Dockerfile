# 1. Builder stage for installing dependencies
FROM python:3.11-slim as builder

# Install build-time dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && \
    apt-get -y clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install python dependencies
RUN python -m pip install --upgrade pip
COPY requirements.txt .
COPY setup.py .
COPY VERSION .
COPY README.md .
RUN pip wheel --no-cache-dir --wheel-dir=/app/wheels -r requirements.txt .

# 2. Final stage for the application
FROM python:3.11-slim

# Install runtime dependencies (curl for healthcheck, postgres client)
RUN apt-get update && apt-get install -y --no-install-recommends curl postgresql-client && \
    apt-get -y clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_SKIP_DOTENV=1
ENV FLASK_APP=alerta

EXPOSE 8080
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
