FROM python:3.11-slim

# Install curl and build tools
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set Python environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /home/ubuntu/deploy-projects/f88653008ea47d61c436625d

# Copy and install requirements (CPU-compatible versions)
# Note: For GPU support, use nvidia-pytorch base image instead
COPY requirements.txt .

# Install torch and core dependencies (CPU version)
# flash_attn, xformers require CUDA - we'll skip them for CPU-only setup
RUN pip install --no-cache-dir \
    torch==2.7.0 \
    torchaudio==2.7.0 \
    torchvision==0.22.0 \
    torchdata==0.11.0 \
    accelerate==1.9.0 \
    transformers==4.52.0 \
    "ray[data,train,tune,serve]" \
    vllm==0.9.2 \
    hydra-core==1.3.2 \
    omegaconf==2.3.0 \
    liger_kernel==0.6.0 \
    tokenizers==0.21.2

# Install remaining dependencies (excluding GPU-specific packages, dbus-python, numpy, and pandas)
RUN grep -vE '^(torch|torchaudio|torchvision|torchdata|flash_attn|xformers|transformer_engine|numpy|pandas)==' requirements.txt | \
    grep -vE '^(nvidia-|cupy-)' | \
    grep -v '^dbus-python' >> requirements_min.txt && \
    pip install --no-cache-dir -r requirements_min.txt && \
    rm requirements_min.txt

# Install numpy and pandas together to ensure ABI compatibility
RUN pip install --no-cache-dir 'numpy==2.0.2' 'pandas==2.2.3'

# Copy application code
COPY . .

# Install the package in editable mode
RUN pip install -e .

# Set environment variables from context
ENV TORCH_NCCL_AVOID_RECORD_STREAMS=1 \
    CUDA_VISIBLE_DEVICES=""

# Expose default port for potential vLLM/Ray dashboard
EXPOSE 8000

# Healthcheck for training process
HEALTHCHECK --interval=60s --timeout=30s --start-period=120s --retries=3 \
    CMD python -c "import verl" && curl -f http://localhost:8000/health || exit 1

# Default command - will be overridden by docker-compose command
CMD ["python", "-c", "import verl; print('VERL module imported successfully')"]