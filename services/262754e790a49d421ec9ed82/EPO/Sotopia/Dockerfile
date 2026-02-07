# Dockerfile for Sotopia FastAPI service
FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Define environments
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install essential dependencies for the FastAPI server
# Using compatible versions: redis-om[async] supports pydantic 2.x
RUN pip config set global.index-url "https://pypi.org/simple" && \
    pip config set global.extra-index-url "https://pypi.org/simple" && \
    python -m pip install --upgrade pip && \
    pip install --no-cache-dir \
        "fastapi>=0.100.0" \
        "uvicorn[standard]>=0.23.0" \
        "redis>=5.0.0" \
        "redis-om[async]>=0.3.0" \
        "pydantic>=2.0.0" \
        "pydantic-settings>=2.0.0" \
        "starlette>=0.27.0" \
        "python-multipart>=0.0.6" \
        "httpx>=0.24.0" \
        "pytest>=7.0.0"

# Copy application source
COPY sotopia-chat /app/sotopia-chat
COPY sotopia /app/sotopia

# Expose port 8000 for the API service
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Run the FastAPI server
WORKDIR /app/sotopia-chat
CMD ["uvicorn", "fastapi_server:app", "--host", "0.0.0.0", "--port", "8000"]