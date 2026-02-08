FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=all
ENV LOCAL_RANK=0
ENV WORLD_SIZE=1

# Install build dependencies and runtime libraries
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    cmake \
    git \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/61585d678a430d1165ea2cec

# Install pytorch first with compatible numpy
RUN pip install --no-cache-dir "torch==1.13.1" torchvision "numpy<2"

# Install pytorch3d from source (to a permanent location)
RUN git clone --depth 1 --branch v0.7.4 https://github.com/facebookresearch/pytorch3d.git /tmp/pytorch3d && \
    cd /tmp/pytorch3d && \
    pip install --no-cache-dir . && \
    cd /home/ubuntu/deploy-projects/61585d678a430d1165ea2cec && rm -rf /tmp/pytorch3d

# Copy requirements and install remaining dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir "numpy<2" einops hydra-core omegaconf timm wandb plotly scipy opencv-python matplotlib black dash fvcore imageio imageio-ffmpeg iopath ipdb ipython isort jupyter jupyter-black jupyter-dash flask

# Copy project files
COPY . .

# Make start script executable
RUN chmod +x start.sh

CMD ["./start.sh"]