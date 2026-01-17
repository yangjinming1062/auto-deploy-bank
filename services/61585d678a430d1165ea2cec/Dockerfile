FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    git \
    curl \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglx-mesa0 \
    mesa-utils \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install base Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install PyTorch3D from GitHub (no-build-isolation to use installed torch)
RUN pip install --no-cache-dir --no-build-isolation git+https://github.com/facebookresearch/pytorch3d.git

# Copy application code
COPY . .

# Default command (verify environment)
CMD ["python", "-c", "import torch; import cv2; from accelerate import Accelerator; print('Environment OK')"]