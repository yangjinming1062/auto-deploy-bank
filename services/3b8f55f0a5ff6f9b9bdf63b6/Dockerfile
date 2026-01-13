# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: Apache-2.0

FROM python:3.10-slim

# Install system dependencies including curl for healthcheck and build tools for DeepSpeed
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MII_CACHE_PATH=/tmp/mii_cache
ENV MII_HF_CACHE_EXPIRATION=3600
ENV MII_DEBUG_MODE=0
ENV MII_DEBUG_DEPLOY_KEY=
ENV MII_DEBUG_BRANCH=main
ENV WORLD_SIZE=1
ENV LOCAL_RANK=0
ENV RANK=0
ENV MASTER_ADDR=localhost
ENV MASTER_PORT=29500
ENV TRANSFORMERS_CACHE=
ENV HF_HOME=
ENV AZUREML_MODEL_DIR=
ENV SSL_KEYFILE=
ENV SSL_CERTFILE=
ENV HF_AUTH_TOKEN=

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package
RUN pip install .

# Expose the service port
EXPOSE 50050

# Health check - verify the service is running
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:50050/ || exit 1

# Run the service
CMD ["python", "simple_server.py"]