FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ \
    gcc \
    libc6-dev \
    make \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package in development mode
RUN python setup.py develop

# Set default environment variables
ENV PROTENIX_DATA_ROOT_DIR=/af3-dev/release_data/ \
    CUDA_VISIBLE_DEVICES="" \
    CUDA_DEVICE_ORDER=PCI_BUS_ID \
    CUTLASS_PATH="" \
    LAYERNORM_TYPE="" \
    TRIANGLE_ATTENTION="" \
    TRIANGLE_MULTIPLICATIVE="" \
    RANK="0" \
    LOCAL_RANK="0" \
    WORLD_SIZE="1" \
    LOCAL_WORLD_SIZE="1" \
    NCCL_TIMEOUT_SECOND="600" \
    WANDB_API_KEY="" \
    WANDB_CONSOLE="off" \
    MMSEQS_SERVICE_HOST_URL="https://protenix-server.com/api/msa"

# Default command - keep container running for interactive CLI use
CMD ["tail", "-f", "/dev/null"]