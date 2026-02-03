# Simplified Dockerfile for ListSync FastAPI Backend
FROM python:3.9-slim

WORKDIR /usr/src/app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    RUNNING_IN_DOCKER=true

# Copy requirements files
COPY requirements.txt .
COPY api_requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt -r api_requirements.txt

# Copy application source
COPY list_sync ./list_sync
COPY start_api.py .
COPY api_server.py .

# Create a script to initialize and start the service
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Expose ports
EXPOSE 4222 3222

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:4222/api/system/health || exit 1

# Use entrypoint script
ENTRYPOINT ["/docker-entrypoint.sh"]

# Start the API server
CMD ["python", "start_api.py"]