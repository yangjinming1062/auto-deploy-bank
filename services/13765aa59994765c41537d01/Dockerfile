FROM python:3.10-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TORCH_HOME=/tmp
ENV MASTER_PORT=40418
ENV MASTER_ADDR=127.0.0.1
ENV WORLD_SIZE=1
ENV RANK=0
ENV LOCAL_RANK=0
ENV LOCAL_WORLD_SIZE=1
ENV PYTHONHASHSEED=0

# Create working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install FastAPI and uvicorn for web service
RUN pip install --no-cache-dir fastapi uvicorn

# Copy application code
COPY . .

# Install the package in development mode
RUN pip install --no-build-isolation -e .

# Expose port
EXPOSE 40418

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:40418/health || exit 1

# Default command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "40418"]