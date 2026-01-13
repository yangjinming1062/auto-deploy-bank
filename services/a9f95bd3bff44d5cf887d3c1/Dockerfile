# Use Python 3.10 slim base image (Ray supports 3.9-3.13, using 3.10 for compatibility)
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    RAY_DISABLE_DOCKER_CPU_WARNING=1 \
    RAY_DASHBOARD_HOST=0.0.0.0 \
    RAY_DEFAULT_DASHBOARD_PORT=8265

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Install Ray from pre-built wheel to avoid Bazel dependency
# This uses the latest Ray wheel from PyPI which includes pre-compiled binaries
RUN pip install --no-cache-dir "ray[all]"

# Copy requirements file to install additional dependencies
COPY python/requirements.txt .

# Install additional Python dependencies from requirements.txt
# These are installed after Ray to avoid conflicts
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose ports: 8000 for Ray Serve, 8265 for Dashboard
EXPOSE 8000 8265

# Health check for the application
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start Ray Serve application using the start script
CMD ["./start-ray-serve.sh"]