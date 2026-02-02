FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Install system dependencies for opencv and curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxi6 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/75355b239ac485d9d9a8f4af

# Copy requirements first for better caching
COPY requirements.txt .

# Install PyTorch with CUDA support first (special handling for CUDA wheel)
RUN pip install --no-cache-dir \
    torch torchvision \
    --index-url https://download.pytorch.org/whl/cu118

# Install remaining dependencies
RUN pip install --no-cache-dir \
    PyYAML \
    numpy \
    opencv-python \
    tensorboardX \
    matplotlib \
    scipy \
    Pillow \
    joblib \
    lmdb

# Copy the entire project
COPY . .

# Copy and set up entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Healthcheck for web server
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://127.0.0.1:40133/status || exit 1

# Default command - training with SR options
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "codes/train.py", "-opt", "codes/options/sr/train_sr.yml"]