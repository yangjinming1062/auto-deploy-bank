FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/f82e5c7d9a560ea1a701503e

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy application code first (needed for -e . install)
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Expose the internal port
EXPOSE 8000

# Run the server
CMD ["python", "server.py"]