FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    pkg-config \
    libprotobuf-dev \
    libsentencepiece-dev \
    python3-sentencepiece \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch && \
    pip install --no-cache-dir transformers && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt || \
    (sed -i '/torch/d; /transformers/d; /flash-attn/d' requirements.txt && \
     pip install --no-cache-dir -r requirements.txt && \
     pip install --no-cache-dir flash-attn || true)

# Copy application code
COPY . .

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set GPU environment variables
ENV CUDA_DEVICE_ORDER=PCI_BUS_ID
ENV CUDA_VISIBLE_DEVICES=0
ENV TF_GPU_THREAD_MODE=gpu_private
ENV TF_CPP_MIN_LOG_LEVEL=0
ENV TF_FORCE_GPU_ALLOW_GROWTH=true
ENV XLA_PYTHON_CLIENT_MEM_FRACTION=0.65

# Set W&B and Accelerate environment variables
ENV WANDB_API_KEY=
ENV WANDB_PROJECT=
ENV ACCELERATE_LOG_LEVEL=

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "app.py"]