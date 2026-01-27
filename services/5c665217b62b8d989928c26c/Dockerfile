FROM nvidia/cuda:11.3.1-base-ubuntu20.04

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies (Python, pip, build tools, and utilities)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    wget \
    ca-certificates \
    build-essential \
    cmake \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create python symlink
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Create working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
# Install protobuf first for compatibility, then numpy and scipy
RUN pip install --no-cache-dir \
        protobuf==3.20.3 \
        numpy==1.23.3 \
        scipy==1.9.1

# Install PyTorch with CUDA 11.3 support
RUN pip install --no-cache-dir \
        torch==1.12.1+cu113 \
        torchvision==0.13.1+cu113 \
        torchaudio==0.12.1+cu113 \
        -f https://download.pytorch.org/whl/cu113/torch_stable.html

# Install remaining requirements
RUN pip install --no-cache-dir \
        ballpark==1.4.0 \
        einops==0.3.0 \
        h5py==3.7.0 \
        hydra-core==1.3.1 \
        imageio==2.9.0 \
        imageio-ffmpeg==0.4.2 \
        imgaug==0.2.6 \
        imgviz==1.6.2 \
        lightning-utilities==0.5.0 \
        matplotlib==3.5.3 \
        matplotlib-inline==0.1.6 \
        omegaconf>=2.2 \
        opencv-python-headless==4.6.0.66 \
        pandas>=1.5.0 \
        Pillow==9.2.0 \
        plotly==5.7.0 \
        pypng==0.20220715.0 \
        randomname==0.2.1 \
        pytorch-lightning==1.8.6 \
        rich==12.5.1 \
        scikit-image==0.19.3 \
        tabulate==0.9.0 \
        tensorboard==2.9.0 \
        tensorboard-data-server==0.6.1 \
        tensorboard-plugin-wit==1.8.1 \
        tensorboardX==2.5.1 \
        termcolor==2.2.0 \
        torch-efficient-distloss==0.1.3 \
        torch-fidelity==0.3.0 \
        torchmetrics==0.11.0 \
        torchtyping==0.1.4 \
        tornado==6.2 \
        tqdm==4.64.1 \
        transforms3d==0.4.1 \
        trimesh==3.18.0 \
        wandb==0.13.4

# Install torch-scatter for CUDA 11.3 (try multiple PyG wheel URLs)
RUN pip install --no-cache-dir torch-scatter==2.1.0+pt112cu113 \
    -f https://data.pyg.org/whl/torch-1.12.0+cu113.html \
    || pip install --no-cache-dir torch-scatter==2.1.0+pt112cu113 \
    -f https://data.pyg.org/whl/torch-1.12.0.html \
    || pip install --no-cache-dir torch-scatter

# Force reinstall protobuf to fix tensorboardX compatibility (must be after other installs)
RUN pip install --no-cache-dir --force-reinstall protobuf==3.20.3

# Copy application code
COPY . .

# Set default command to run training
CMD ["python", "trainer/train_panopli_tensorf.py"]