# Build stage for building Python dependencies and CUDA extensions
FROM nvidia/cuda:12.1.1-devel-ubuntu22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3-pip \
    python3-venv \
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    git \
    wget \
    libeigen3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

WORKDIR /workspace

# Set CUDA arch list for efficient builds
ENV TORCH_CUDA_ARCH_LIST="7.0;8.0;8.6;8.9;9.0"
ENV MAX_JOBS=4

# Upgrade pip, wheel, setuptools first
RUN pip install --no-cache-dir --upgrade pip wheel setuptools

# Install PyTorch with CUDA support (use pre-built wheels)
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Copy requirements and install lightweight deps first (faster, better cache)
COPY requirements.txt .

# Install core dependencies in smaller groups for better caching and failure isolation
RUN pip install --no-cache-dir einops omegaconf opencv-python ninja \
    && pip install --no-cache-dir trimesh==4.2.0 scikit-learn tqdm jaxtyping==0.2.31 \
    && pip install --no-cache-dir transformers==4.40.1 diffusers==0.19.3 \
    && pip install --no-cache-dir open_clip_torch imageio imageio-ffmpeg onnxruntime \
    && pip install --no-cache-dir PyMCubes libigl pygltflib xatlas rembg gradio gradio-litmodel3d==0.0.1 \
    && pip install --no-cache-dir pymeshlab huggingface_hub

# Copy source code BEFORE heavy builds
COPY install.sh .
COPY start.sh .
COPY app.py .
COPY app_fallback.py .
COPY inference.py .
COPY nvdiffrast/ nvdiffrast/
COPY cubvh/ cubvh/
COPY xformers/ xformers/
COPY dva/ dva/
COPY simple_knn/ simple_knn/
COPY models/ models/
COPY configs/ configs/
COPY scripts/ scripts/
COPY datasets/ datasets/
COPY utils/ utils/
COPY assets/ assets/

# Make scripts executable
RUN chmod +x install.sh start.sh

# Note: CUDA extensions (mvpraymarch, utils, simple-knn) require GPU/CUDA
# and are provided via mock modules for CPU-only environments

# Final runtime stage
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    python3-full \
    libgl1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libopengl0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libeigen3-dev \
    curl \
    git \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Create venv and install Python deps
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Copy pre-built Python environment and compiled extensions
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /workspace /workspace

WORKDIR /workspace

# Healthcheck
HEALTHCHECK --interval=60s --timeout=30s --start-period=180s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Expose the Gradio port
EXPOSE 7860

# Start the application
CMD ["./start.sh"]