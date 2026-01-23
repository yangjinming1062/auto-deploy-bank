FROM python:3.10-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/6127593a9944c99237f21d2d

# Set Python environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/home/ubuntu/deploy-projects/6127593a9944c99237f21d2d

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose internal port (Flask wrapper)
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Default command - run Flask wrapper
CMD ["python", "app.py"]