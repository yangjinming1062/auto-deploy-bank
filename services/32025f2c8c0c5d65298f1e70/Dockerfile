FROM python:3.10-slim

# Install curl and build tools for Python packages
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/32025f2c8c0c5d65298f1e70

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose internal port
EXPOSE 8080

# Run the Flask application
CMD ["python", "bing_search_cache_server.py"]