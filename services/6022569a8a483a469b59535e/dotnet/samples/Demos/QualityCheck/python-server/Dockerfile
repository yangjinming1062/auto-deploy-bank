# Copyright (c) Microsoft. All rights reserved.

FROM python:3.10-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/6022569a8a483a469b59535e

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose the internal port
EXPOSE 8000

# Run the FastAPI application with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]