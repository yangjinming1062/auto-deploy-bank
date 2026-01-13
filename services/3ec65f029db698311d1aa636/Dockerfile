# Root-level Dockerfile for speculative_kd web service
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    pkg-config \
    libsentencepiece-dev \
    libprotobuf-dev \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy web requirements
COPY speculative_kd/requirements-web.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch && \
    pip install --no-cache-dir transformers && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir alignment && \
    pip install --no-cache-dir accelerate && \
    pip install --no-cache-dir trl && \
    pip install --no-cache-dir pandas && \
    pip install --no-cache-dir matplotlib && \
    pip install --no-cache-dir scikit-learn && \
    pip install --no-cache-dir wandb && \
    pip install --no-cache-dir datasets && \
    pip install --no-cache-dir numpy && \
    pip install --no-cache-dir deepspeed

# Copy application code
COPY speculative_kd/ ./speculative_kd/

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set GPU environment variables
ENV XLA_PYTHON_CLIENT_MEM_FRACTION=0.65
ENV TF_GPU_THREAD_MODE=gpu_private
ENV CUDA_DEVICE_ORDER=PCI_BUS_ID
ENV CUDA_VISIBLE_DEVICES=0
ENV TF_CPP_MIN_LOG_LEVEL=0
ENV TF_FORCE_GPU_ALLOW_GROWTH=true

# Set working directory to the app
WORKDIR /app/speculative_kd

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "app.py"]