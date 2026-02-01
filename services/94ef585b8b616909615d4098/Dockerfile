FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/94ef585b8b616909615d4098

# Install whylogs and fastapi with dependencies
# Pin numpy to <2.0 to avoid compatibility issues with whylogs
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
    "numpy<2.0" \
    whylogs \
    fastapi \
    uvicorn \
    pandas \
    orjson

# Copy application code
COPY server.py .

# Expose internal port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the server using python server.py
CMD ["python", "server.py"]