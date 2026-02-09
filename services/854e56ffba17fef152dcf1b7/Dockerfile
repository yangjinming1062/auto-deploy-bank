# syntax = docker/dockerfile:experimental
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV POUTYNE_RELEASE_BUILD=${POUTYNE_RELEASE_BUILD:-}
ENV CUDA_DEVICE=${CUDA_DEVICE:-0}
ENV MULTI_GPUS=${MULTI_GPUS:-0}
ENV WANDB_MODE=${WANDB_MODE:-}

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /home/ubuntu/deploy-projects/854e56ffba17fef152dcf1b7

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy and install the package
COPY . .
RUN python setup.py install

# Copy health check script
COPY scripts/health_server.py /usr/local/bin/health_server.py
RUN chmod +x /usr/local/bin/health_server.py

# Expose the port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the health check server
CMD ["python", "/usr/local/bin/health_server.py", "8080"]