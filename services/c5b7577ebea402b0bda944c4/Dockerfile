FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/c5b7577ebea402b0bda944c4

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
# Pin setuptools to fix gym 0.21.0 compatibility
RUN pip install --no-cache-dir setuptools==65.5.1
RUN pip install --no-cache-dir -r requirements.txt

# Install Flask for service wrapper
RUN pip install --no-cache-dir flask

# Copy application code
COPY . .

# Expose the service port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start the service
CMD ["python", "service.py"]