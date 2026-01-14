# Multi-stage build for Katib UI - Simplified static version without Kubernetes
# This version serves a static UI for demonstration purposes

# Stage 1: Python web server
FROM python:3.11-slim AS web-server
WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Copy the server script
COPY server.py /app/server.py

# Expose port 8080
EXPOSE 8080

# Health check using curl to check if server responds
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl --no-progress-meter --fail --connect-timeout 5 http://localhost:8080/ || exit 1

# Set the entrypoint to run the Python web server
ENTRYPOINT ["python3", "/app/server.py"]