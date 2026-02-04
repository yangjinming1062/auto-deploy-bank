FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=""
ENV TORCH_CUDA_ARCH_LIST="8.0;8.6;8.9;9.0"
ENV FORCE_CUDA="0"
ENV DETECTRON2_DATASETS=/home/appuser/datasets

# Install system dependencies and curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    g++ \
    cmake \
    libgl1 \
    libglx-mesa0 \
    libglapi-mesa \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/appuser

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Clone and install detectron2 from source
RUN git clone --depth 1 https://github.com/facebookresearch/detectron2.git /tmp/detectron2
WORKDIR /tmp/detectron2
RUN pip install --no-cache-dir -e .
WORKDIR /home/appuser

# Copy application code
COPY . .

# Create cache directories and datasets directory
RUN mkdir -p /tmp && mkdir -p /home/appuser/.cache && mkdir -p /home/appuser/datasets

# Download GLEE model weights (Lite model is ~1GB, Plus model is ~3GB)
RUN curl -L -o GLEE_Lite_joint.pth "https://huggingface.co/spaces/Junfeng5/GLEE_demo/resolve/main/MODEL_ZOO/GLEE_Lite_joint.pth" 2>/dev/null || \
    wget -O GLEE_Lite_joint.pth "https://huggingface.co/spaces/Junfeng5/GLEE_demo/resolve/main/MODEL_ZOO/GLEE_Lite_joint.pth" 2>/dev/null || \
    echo "Warning: Could not download GLEE_Lite_joint.pth"

RUN curl -L -o GLEE_Plus_joint.pth "https://huggingface.co/spaces/Junfeng5/GLEE_demo/resolve/main/MODEL_ZOO/GLEE_Plus_joint.pth" 2>/dev/null || \
    wget -O GLEE_Plus_joint.pth "https://huggingface.co/spaces/Junfeng5/GLEE_demo/resolve/main/MODEL_ZOO/GLEE_Plus_joint.pth" 2>/dev/null || \
    echo "Warning: Could not download GLEE_Plus_joint.pth"

# Download CLIP model weights for text encoder
RUN pip install --no-cache-dir huggingface_hub && \
    python3 -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='openai/clip-vit-base-patch32', local_dir='/home/appuser/projects/GLEE/clip_vit_base_patch32', allow_patterns=['*.safetensors', '*.bin', '*.json'])" 2>/dev/null || \
    echo "Warning: Could not download CLIP model weights"

# Download Swin-L backbone weights for Plus model (~2.5GB)
RUN curl -L -o weights/swin_large_patch4_window12_384_22k.pth "https://huggingface.co/microsoft/Swin-Large/resolve/main/pytorch_model.bin" 2>/dev/null || \
    wget -O weights/swin_large_patch4_window12_384_22k.pth "https://huggingface.co/microsoft/Swin-Large/resolve/main/pytorch_model.bin" 2>/dev/null || \
    echo "Warning: Could not download Swin-L backbone weights"

CMD ["python", "app.py"]