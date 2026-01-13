# Use a slim Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 8080

# Command to run the application
CMD ["python", "run.py"]
