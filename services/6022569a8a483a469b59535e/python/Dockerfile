FROM python:3.12-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/6022569a8a483a469b59535e

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install build dependencies
RUN pip install --no-cache-dir flit-core

# Copy the package source and metadata first
COPY pyproject.toml README.md LICENSE ./
COPY semantic_kernel/ ./semantic_kernel/

# Install the semantic-kernel package with all dependencies
# This installs pybars4 first (required by the package), then installs the package with all deps
RUN pip install --no-cache-dir "pybars4 ~= 0.9" && \
    pip install --no-cache-dir .

# Install dapr dependencies separately (they're optional for the demo)
RUN pip install --no-cache-dir "dapr>=1.14.0" "dapr-ext-fastapi>=1.14.0" "flask-dapr>=1.14.0"

# Copy remaining application code
COPY app.py .

# Expose the internal port
EXPOSE 5001

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5001/healthz || exit 1

# Run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5001"]