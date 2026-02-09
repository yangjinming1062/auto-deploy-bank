FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    cmake \
    git \
    libgl1 \
    libglapi-mesa \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/home/ubuntu/deploy-projects/1d975e07b1e87c514c26a788
ENV CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-}
ENV D_NERF_BASEDIR=/home/ubuntu/deploy-projects/1d975e07b1e87c514c26a788/logs
ENV D_NERF_DATADIR=/home/ubuntu/deploy-projects/1d975e07b1e87c514c26a788/data
ENV D_NERF_DATASET_TYPE=llff
ENV D_NERF_NERF_TYPE=direct_temporal
ENV D_NERF_LRATE=0.01
ENV D_NERF_N_ITER=800000
ENV D_NERF_DO_HALF_PRECISION=False

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/1d975e07b1e87c514c26a788

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project and install torchsearchsorted
COPY torchsearchsorted ./torchsearchsorted
RUN cd torchsearchsorted && pip install .

# Copy rest of the project
COPY . .

# Create necessary directories
RUN mkdir -p /home/ubuntu/deploy-projects/1d975e07b1e87c514c26a788/logs /home/ubuntu/deploy-projects/1d975e07b1e87c514c26a788/data

# Healthcheck - verify Python and main modules can be imported
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["python", "-c", "import sys; import torch; from run_dnerf_helpers import *; print('Health check passed'); sys.exit(0)"]

# Run the D-NeRF training script
CMD ["python", "run_dnerf.py"]