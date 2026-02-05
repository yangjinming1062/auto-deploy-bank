# SNIPER Object Detection Service
# Based on MXNet deep learning framework

FROM python:3.9-slim

# Install curl for healthcheck and required libraries
RUN apt-get update && apt-get install -y \
    curl \
    libgfortran5 \
    libopenblas-dev \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/00bb5a0685372be6bb3bd49d

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MXNET_CUDNN_AUTOTUNE_DEFAULT=0
ENV CUDA_HOME=/usr/local/cuda
ENV CUDA_PATH=/usr/local/cuda
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
ENV MXNET_CPU_WORKER_NTHREADS=4

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt || \
    pip install --no-cache-dir opencv-python Cython matplotlib numpy scipy pyyaml \
    EasyDict protobuf argparse scikit-image tqdm flask Pillow requests mxnet

# Copy application code
COPY . .

# Expose the service port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start the Flask API service
CMD ["python", "api.py"]