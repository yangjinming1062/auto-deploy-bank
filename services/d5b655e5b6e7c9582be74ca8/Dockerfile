FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/d5b655e5b6e7c9582be74ca8

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN pip install --no-cache-dir 'pydantic>=2.4.0,<2.7.0' fastapi>=0.103.1 'uvicorn[standard]>=0.25.0' structlog>=23.1.0 psutil>=5.9.8 aiofiles>=23.2.1 aiohttp>=3.9.5 tenacity>=8.4.2 'databases[aiomysql,aiosqlite]>=0.9.0' transformers>=4.44.0

# Copy application code
COPY sandbox/ ./sandbox/
COPY scripts/ ./scripts/
COPY docs/ ./docs/
COPY pyproject.toml .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SANDBOX_CONFIG=local
ENV HOST=0.0.0.0
ENV PORT=8080

# Expose the internal port
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/v1/ping || exit 1

# Start command
CMD ["uvicorn", "sandbox.server.server:app", "--host", "0.0.0.0", "--port", "8080"]