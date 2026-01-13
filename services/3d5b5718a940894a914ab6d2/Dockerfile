# Dockerfile for BentoML Service

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app:$PYTHONPATH"

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and source code
COPY README.md pyproject.toml ./
COPY src/ src/
# Install BentoML from the source code in editable mode
RUN pip install --no-cache-dir -e .

# Copy application code
COPY . .

# Create bentos directory for BentoML
RUN mkdir -p /app/bentos

# Expose the internal port (3000 from bentoml.yaml)
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:3000/healthz || exit 1

# Start the BentoML service
CMD ["bentoml", "serve", "/app", "--host", "0.0.0.0", "--port", "3000", "--production"]