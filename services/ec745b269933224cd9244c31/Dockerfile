FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000
ENV FLASK_ENV=production

# Install system dependencies (g++ and cmake needed for grpcio-tools and pyarrow)
RUN apt-get update && apt-get install -y \
    curl \
    g++ \
    cmake \
    python3-dev \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/ec745b269933224cd9244c31

# Copy requirements first for better caching
COPY requirements-service.txt .

# Install Python dependencies (using minimal set for runtime service)
RUN pip install --no-cache-dir -r requirements-service.txt

# Copy application code
COPY . .

# Expose the port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the Flask application
CMD ["python", "app.py"]