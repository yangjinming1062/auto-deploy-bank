FROM python:3.11-slim

WORKDIR /app

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy application code and install dependencies
COPY . .
RUN pip install --no-cache-dir .

# Create a directory for the database
RUN mkdir /data

# Expose the internal port
EXPOSE 8080
