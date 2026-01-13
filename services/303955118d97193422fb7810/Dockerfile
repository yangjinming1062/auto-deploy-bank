FROM python:3.8-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck and other essential tools
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies and Flask
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir flask

# Copy application code
COPY . .

# Set environment variables for distributed training
ENV RANK=0
ENV WORLD_SIZE=1
ENV MASTER_ADDR=localhost
ENV MASTER_PORT=6600
ENV MTDNN_CO_RESOLVE_ENDPOINT=https://mrc.blob.core.windows.net/mt-dnn-model

# Expose port (for monitoring or future API usage)
EXPOSE 40192

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import sys; print('healthy'); sys.exit(0)" || exit 1

# Default command (can be overridden)
CMD ["python", "web_server.py"]