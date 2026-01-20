FROM python:3.10-slim

# Install curl and procps for healthcheck
RUN apt-get update && apt-get install -y curl procps && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/76275e5ba3e942ff7fe5bb00

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Create data directory for output
RUN mkdir -p /data

# Default command for training
ENTRYPOINT ["./entrypoint.sh"]