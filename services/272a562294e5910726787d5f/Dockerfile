FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    git-lfs \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set Python environment
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create app directory
WORKDIR /home/ubuntu/deploy-projects/272a562294e5910726787d5f

# Install torch first (required by flash-attn)
# For GPU support, use CUDA index URL instead, e.g.:
# --index-url https://download.pytorch.org/whl/cu118
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install accelerate for model loading on CPU
RUN pip install --no-cache-dir accelerate

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies (skip flash-attn as it requires CUDA)
# flash-attn is optional for performance optimization
RUN grep -v '^flash-attn' requirements.txt > requirements_no_flash.txt && \
    pip install --no-cache-dir -r requirements_no_flash.txt && \
    rm requirements_no_flash.txt

# Copy application code
COPY . .

# Default command - will be overridden by docker-compose or run command
CMD ["python", "inference.py"]