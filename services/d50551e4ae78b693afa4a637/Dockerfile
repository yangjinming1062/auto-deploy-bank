# MOFA-Video Docker Configuration
# Using CUDA-enabled Python base image for GPU support

FROM ubuntu:22.04

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    CUDA_HOME=/usr/local/cuda \
    CUDA_VISIBLE_DEVICES=0 \
    NVIDIA_VISIBLE_DEVICES=0 \
    TORCH_HOME=/root/.cache/torch \
    PYTHONHASHSEED=42 \
    PATH=/usr/local/cuda/bin:$PATH

# Install system dependencies and CUDA toolkit
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
    vim \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    ffmpeg \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    python3 \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install CUDA toolkit from NVIDIA repository
RUN wget -q https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb && \
    dpkg -i cuda-keyring_1.1-1_all.deb && \
    apt-get update && \
    apt-get install -y --no-install-recommends cuda-toolkit-12-0 && \
    rm -rf /var/lib/apt/lists/* && \
    rm cuda-keyring_1.1-1_all.deb

# Create working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY MOFA-Video-Hybrid/requirements.txt .

# Install Python dependencies
# Pin huggingface_hub to <0.20.0 because cached_download was removed in 0.20.0
RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir 'huggingface_hub<0.20.0' && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY MOFA-Video-Hybrid/ .

# Create directory for model checkpoints
RUN mkdir -p ckpts/mofa/traj_controlnet \
            ckpts/mofa/ldmk_controlnet \
            ckpts/mofa/stable-video-diffusion-img2vid-xt-1-1 \
            ckpts/aniportrait \
            ckpts/sad_talker \
            ckpts/gfpgan

# Create output directory
RUN mkdir -p Output_audio_driven Output_video_driven

# Expose the application port
EXPOSE 9080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:9080/ || exit 1

# Start the application
CMD ["python3", "run_gradio_audio_driven.py"]