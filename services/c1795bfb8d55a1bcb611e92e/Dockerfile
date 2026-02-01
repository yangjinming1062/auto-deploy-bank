FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/c1795bfb8d55a1bcb611e92e

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/home/ubuntu/deploy-projects/c1795bfb8d55a1bcb611e92e

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install vescale package
RUN pip install -e .

# Expose the service port
EXPOSE 41676

# Default command: run the health service
CMD ["python", "/home/ubuntu/deploy-projects/c1795bfb8d55a1bcb611e92e/health_server.py"]