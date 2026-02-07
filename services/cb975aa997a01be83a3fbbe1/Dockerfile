FROM python:3.10-slim

WORKDIR /home/ubuntu/deploy-projects/cb975aa997a01be83a3fbbe1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set Python environment variables
ENV PYTHONUNBUFFERED=1

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Default command - run the Flask API server
CMD ["python", "api_server.py"]