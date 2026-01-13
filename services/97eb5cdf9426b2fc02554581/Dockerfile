# Simple Dockerfile for MaxText mock server
FROM python:3.12-slim

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install only the essential packages for the mock server
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    fastapi==0.122.0 \
    uvicorn==0.38.0

# Expose internal port
EXPOSE 9000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:9000/health || exit 1

# Start the mock inference server
CMD ["python3", "src/MaxText/maxengine_server_mock.py"]