FROM python:3.10-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TOKENIZERS_PARALLELISM=true
ENV CUDA_LAUNCH_BLOCKING=1
ENV CUBLAS_WORKSPACE_CONFIG=:16:8
ENV RANK=-1
ENV NCCL_P2P_DISABLE=1
ENV NCCL_DEBUG=INFO

WORKDIR /home/ubuntu/deploy-projects/cc3f5f129c23f686bec807f3

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 40524

# Run the health service with Flask
CMD ["python", "-c", "from health_service import app; app.run(host='0.0.0.0', port=40524)"]