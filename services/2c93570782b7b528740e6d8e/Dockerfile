FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install curl, git, and libsnappy for python-snappy
RUN apt-get update && apt-get install -y curl git libsnappy-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/skyline/github/skyline

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create required directories
RUN mkdir -p /var/log/skyline /var/run/skyline /tmp/skyline

# Expose the webapp port
EXPOSE 1500

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:1500/ || exit 1

# Start command using gunicorn with the custom config
CMD ["gunicorn", "--config", "skyline/webapp/gunicorn.py", "webapp:app"]