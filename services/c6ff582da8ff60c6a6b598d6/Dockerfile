FROM python:3.9-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY Requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r Requirements.txt

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 8000

# Healthcheck using curl
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the Flask application
CMD ["python", "app.py"]