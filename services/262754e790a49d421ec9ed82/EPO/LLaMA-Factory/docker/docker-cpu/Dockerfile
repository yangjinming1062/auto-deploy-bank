# CPU-based Dockerfile for LLaMA-Factory API service
FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Define environments
ENV PYTHONUNBUFFERED=1
ENV MAX_JOBS=4
ENV DISABLE_VERSION_CHECK=1

# Copy requirements first for better caching
COPY requirements.txt /app/
RUN pip config set global.index-url "https://pypi.org/simple" && \
    pip config set global.extra-index-url "https://pypi.org/simple" && \
    python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . /app/

# Install the LLaMA Factory package in editable mode with metrics extras
RUN pip install -e ".[metrics]"

# Expose port 8000 for the API service
ENV API_PORT=8000
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Run the API server
CMD ["python", "src/api.py"]