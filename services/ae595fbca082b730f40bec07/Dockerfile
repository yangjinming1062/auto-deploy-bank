FROM python:3.11-slim

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/ae595fbca082b730f40bec-app

# Install system dependencies and curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt .
COPY slack/requirements.txt ./slack/

# Create a modified requirements file with psycopg2-binary instead of psycopg2
RUN sed 's/^psycopg2$/psycopg2-binary/' requirements.txt > requirements-binary.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-binary.txt && \
    pip install --no-cache-dir gunicorn && \
    pip install --no-cache-dir -r slack/requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=slack/app.py
ENV PORT=5000

# Expose the internal port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/slack/events || exit 1

# Start the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "600", "--chdir", "slack", "app:flask_app"]