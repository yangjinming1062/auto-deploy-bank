# Root-level Dockerfile for the Django backend service

FROM python:3.12-slim AS base

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV ALLOWED_HOSTS=*

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend files and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ .

# Create wait-for script for celery services
RUN printf '#!/bin/bash\nmax_attempts=30\nattempt=0\nwhile [ $attempt -lt $max_attempts ]; do\n    python -c "import django; django.setup()" 2>/dev/null && break\n    attempt=$((attempt + 1))\n    sleep 2\ndone\nexec "$@"\n' > /wait_for_db.sh && chmod +x /wait_for_db.sh

EXPOSE 8000

# Use bash wrapper for celery services to wait for Django setup
CMD ["/bin/bash", "-c", "/wait_for_db.sh gunicorn backend.wsgi:application --bind 0.0.0.0:8000"]