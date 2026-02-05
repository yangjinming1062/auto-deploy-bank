# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates.
# Licensed under the Apache License, Version 2.0

FROM python:3.10-slim

WORKDIR /home/ubuntu/deploy-projects/18815cddb1dcb354e2d2c7f0

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set Python environment variables
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/home/ubuntu/deploy-projects/18815cddb1dcb354e2d2c7f0/.cache/huggingface
ENV HF_HUB_DOWNLOAD_EAGER=1

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package in editable mode
RUN pip install -e .

# Expose the port
EXPOSE 7860

# Healthcheck
HEALTHCHECK --interval=30s --timeout=60s --start-period=180s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Start the application
CMD ["python", "app.py", "--port", "7860"]