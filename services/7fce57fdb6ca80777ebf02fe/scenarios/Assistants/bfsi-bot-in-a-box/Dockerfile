FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/backend/ ./src/backend/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the internal port (Flask default 5007)
EXPOSE 5007

# Change to the backend directory and run the app
WORKDIR /app/src/backend
CMD ["python", "app.py"]