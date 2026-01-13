# Use the official Python image.
FROM python:3.11-slim

# Install dependencies for PostgreSQL client and curl
RUN apt-get update && apt-get install -y libpq-dev gcc curl postgresql-client && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt base_requirements.txt ./
RUN python -m pip install --no-cache-dir -r base_requirements.txt -r requirements.txt

# Copy application code
COPY . .

# Overwrite the testing configuration with our robust, environment-based configuration
COPY configuration.py /app/netbox/netbox/configuration_testing.py

# This entrypoint will handle all setup and run the application
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set the final working directory and run the application as per the docs
WORKDIR /app/netbox
