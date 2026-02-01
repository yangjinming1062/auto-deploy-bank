FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy source code first
COPY arkitect/ ./arkitect/
COPY pyproject.toml README.md ./

# Install all dependencies directly from pyproject.toml
# Using pip install with all dependencies listed
# Note: langchain 0.2.x is the last version supporting the old API
RUN pip install --no-cache-dir \
    "langchain-core>=0.1.0,<0.3.0" \
    "langchain>=0.1.0,<0.3.0" \
    "fastapi<1.0.0,>=0.100.0" \
    "uvicorn<0.30.0,>=0.22.0" \
    "opentelemetry-api<2.0.0,>=1.22.0" \
    "pydantic<3.0.0,>=2.0.0" \
    "opentelemetry-exporter-otlp<2.0.0,>=1.22.0" \
    "jinja2<4.0.0,>=3.1.2" \
    "structlog<25.0.0,>=23.1.0" \
    "opentelemetry-sdk<2.0.0,>=1.22.0" \
    "volcengine-python-sdk>=3.0.10" \
    "httpx>=0.27.0" \
    "pytz>=2020.5" \
    "tenacity==8.3.0" \
    "uvloop>=0.19.0" \
    "orjson<3.10.7" \
    "aiofiles==23.2.1" \
    "tos<3.0.0,>=2.8.1" \
    "mcp>=1.8.1" \
    "aiohttp>=3.11.13" \
    "websockets>=14.0" \
    "redis>=6.1.0"

# Copy the example application
COPY examples/agent_framework/ /app/

# Expose the internal port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/v1/ping || exit 1

# Start the application
CMD ["python", "main.py"]