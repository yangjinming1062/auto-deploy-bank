# Use Python 3.10 slim image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV TOKENIZERS_PARALLELISM=false
ENV VLLM_ATTENTION_BACKEND=FLASH_ATTN
ENV RAY_memory_monitor_refresh_ms=0

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install FlashAttention requirements first (these require compilation)
# Note: FlashAttention requires CUDA/cuDNN which may not be available in all environments
# We try to install it, but continue if it fails
COPY flashattn_requirements.txt /tmp/flashattn_requirements.txt
# Try to install FlashAttention, but don't fail if it can't be installed
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/flashattn_requirements.txt || echo "WARNING: FlashAttention installation failed - continuing without GPU optimizations"

# Copy requirements and install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the entire project
WORKDIR /app
COPY . .

# Create data directory for outputs
RUN mkdir -p /app/data

# Default command - runs the training system
# Note: This is a batch training system, not a web service
# Users should override this command with their specific training parameters
CMD ["python", "-m", "absolute_zero_reasoner.main_azr_ppo", "--help"]