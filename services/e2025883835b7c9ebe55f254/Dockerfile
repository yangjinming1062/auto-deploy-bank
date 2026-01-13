# Python base image
FROM python:3.8-slim

LABEL MAINTAINER="Anand Tiwari"

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=archerysecurity.settings.base \
    ALLOWED_HOSTS=*

# Install system dependencies including curl for healthcheck and build tools
RUN apt-get update && apt-get install -y \
    curl \
    postgresql-client \
    gcc \
    g++ \
    python3-dev \
    libffi-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    pkg-config \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*

# Create archerysec user and group
RUN groupadd -r archerysec && useradd -r -m -g archerysec archerysec

# Set user to archerysec
USER archerysec

# Create working directory
WORKDIR /home/archerysec/app

# Copy requirements first for better caching
COPY --chown=archerysec:archerysec requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=archerysec:archerysec . .

# Expose port
EXPOSE 8000

# Include init script
COPY --chown=archerysec:archerysec ./docker-files/init.sh /usr/local/bin/init.sh
RUN chmod +x /usr/local/bin/init.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start application
CMD ["/usr/local/bin/init.sh"]
