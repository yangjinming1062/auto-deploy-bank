FROM python:3.8-slim

# This image is NOT made for production use.
LABEL maintainer="Eero Ruohola <eero.ruohola@shuup.com>"

# Install system dependencies
RUN apt-get update \
    && apt-get --assume-yes install \
        libpangocairo-1.0-0 \
        libjpeg-dev \
        libpng-dev \
        zlib1g-dev \
        curl \
        nodejs \
        npm \
        build-essential \
        python3-dev \
        python-is-python3 \
        git \
    && rm -rf /var/lib/apt/lists/ /var/cache/apt/

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    ALLOWED_HOSTS=* \
    PYTHONPATH=/app \
    PYTHON=python3 \
    NPM_CONFIG_LEGACY_PEER_DEPS=true \
    NPM_CONFIG_FUND=false \
    NPM_CONFIG_AUDIT=false \
    npm_config_ignore_scripts=true

# Set working directory
WORKDIR /app

# Copy source code first (needed for setup.py to work)
COPY . /app

# Install Python dependencies without -e . to avoid build_resources trigger
RUN grep -v "^-e " requirements-tests.txt > /tmp/requirements.txt && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Install node-gyp globally to handle dependencies
RUN npm install -g node-gyp@8.4.1

# Build static resources during image build
RUN python3 setup.py build_resources

# Expose port
EXPOSE 8000

# Add entrypoint script
RUN printf '#!/bin/bash\n\
set -e\n\
echo "Running database migrations..."\n\
python3 -m shuup_workbench migrate --noinput\n\
\n\
# Create default shop if it doesn'\''t exist\n\
echo "Creating default shop..."\n\
python3 -c "\n\
import django\n\
django.setup()\n\
from shuup.core.models import Shop\n\
from django.contrib.auth.models import User\n\
\n\
if not Shop.objects.exists():\n\
    shop = Shop.objects.create(\n\
        name=\"Default Shop\",\n\
        identifier=\"default\",\n\
        currency=\"USD\",\n\
        prices_include_tax=False\n\
    )\n\
    print(f\"Created shop: {shop}\")\n\
else:\n\
    print(\"Shop already exists\")\n\
\n\
# Create superuser if doesn'\''t exist\n\
if not User.objects.filter(username=\"admin\").exists():\n\
    user = User.objects.create_superuser(\"admin\", \"admin@shuup.local\", \"admin\")\n\
    print(f\"Created superuser: {user}\")\n\
else:\n\
    print(\"Superuser already exists\")\n\
"\n\
\n\
echo "Starting server..."\n\
exec python3 -m shuup_workbench runserver 0.0.0.0:8000\n\
' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
