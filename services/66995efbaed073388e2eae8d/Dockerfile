FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV OMP_NUM_THREADS=8
ENV ARROW_DEFAULT_MEMORY_POOL=system

# Install curl for healthcheck and build dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/66995efbaed073388e2eae8d

# Copy requirements first for better caching
COPY setup.py .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy application code
COPY pyquokka/ ./pyquokka/
COPY redis.conf .
COPY apps/ ./apps/
COPY benchmark/ ./benchmark/
COPY docker/ ./docker/

# Expose Arrow Flight port and HTTP health port
EXPOSE 5005

# Healthcheck - using TCP socket check for HTTP endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import socket; s = socket.socket(); s.connect(('localhost', 5006)); s.close()"

# Start the Arrow Flight server with HTTP health endpoint for Quokka
CMD ["python", "docker/server_with_http.py"]