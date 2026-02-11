FROM python:3.10-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY python/pyproject.toml .

# Install dependencies
RUN pip install --no-cache-dir -r /dev/stdin <<EOF
pydantic>=2,<3
requests>=2.0.0
orjson>=3.9.14
httpx>=0.23.0,<1
requests-toolbelt>=1.0.0
zstandard>=0.23.0
packaging>=23.2
uuid-utils>=0.12.0,<1.0
xxhash>=3.0.0
fastapi>=0.115.4
uvicorn>=0.29.0
EOF

# Copy application code
COPY python/langsmith/ ./langsmith/
COPY python/tests/integration_tests/fake_server.py ./fake_server.py

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV OTEL_ENABLED=false

EXPOSE 54773

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -X POST --silent --fail http://localhost:54773/fake-route > /dev/null 2>&1 || exit 1

# Run the FastAPI application
CMD ["uvicorn", "fake_server:fake_app", "--host", "0.0.0.0", "--port", "54773"]