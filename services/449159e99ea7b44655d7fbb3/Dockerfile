# YOLOv5 🚀 by Ultralytics, GPL-3.0 license

# Start FROM Python slim image
FROM python:3.10-slim

# Install curl and OpenCV dependencies
RUN apt-get update && apt-get install -y curl libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Create working directory
WORKDIR /home/ubuntu/deploy-projects/449159e99ea7b44655d7fbb3

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run Flask REST API
CMD ["python", "utils/flask_rest_api/restapi.py", "--port", "5000"]