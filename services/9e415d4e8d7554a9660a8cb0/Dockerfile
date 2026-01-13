# Use python:3.10-slim base image
FROM python:3.10-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl build-essential libmariadb-dev libldap2-dev libsasl2-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set python unbuffered
ENV PYTHONUNBUFFERED=1

# Copy requirements and install dependencies
COPY requirements/ ./requirements/
RUN pip install --no-cache-dir -r requirements/base.txt -r requirements/dev.txt -r requirements/extra.txt gunicorn

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 8080

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "examples.user_registration.run:app"]
