# Dockerfile for VeRL (reinforcement learning) training system
# Base image with CUDA support for PyTorch and vLLM

FROM nvidia/cuda:12.4.1-base-ubuntu22.04

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    VLLM_DISABLE_COMPILE_CACHE=1

# Install system dependencies and Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    curl \
    wget \
    git \
    vim \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3.11 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/60235be3b6db101b31f508e6

# Copy requirements file first for better layer caching
COPY Agent0/requirements.txt .

# Install Python dependencies (excluding outlines, outlines_core, and av due to version/build conflicts)
RUN grep -v '^outlines' requirements.txt | grep -v '^outlines_core' | grep -v '^av==' | pip install --no-cache-dir -r /dev/stdin

# Copy application code
COPY Agent0/curriculum_train ./curriculum_train
COPY Agent0/executor_train ./executor_train
COPY Agent0-VL ./Agent0-VL
COPY health_server.py .

# Set working directory for training
WORKDIR /home/ubuntu/deploy-projects/60235be3b6db101b31f508e6/curriculum_train

# Default command - training entry point
CMD ["python", "-m", "verl.trainer.main", "--help"]