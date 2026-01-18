FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1
ENV KMP_DUPLICATE_LIB_OK=TRUE

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y \
    wget \
    git \
    build-essential \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch with CUDA 11.3
RUN pip install --no-cache-dir torch==1.12.1+cu113 torchvision==0.13.1+cu113 --extra-index-url https://download.pytorch.org/whl/cu113

# Install MMOCR and related packages
RUN pip install --no-cache-dir -U openmim && \
    python -m mim install mmengine && \
    python -m mim install mmocr && \
    python -m mim install 'mmcv==2.0.0rc4' && \
    python -m mim install 'mmdet==3.0.0rc5' && \
    python -m mim install 'mmcls==1.0.0rc5'

# Install SAM and other dependencies
RUN pip install --no-cache-dir git+https://github.com/facebookresearch/segment-anything.git

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir huggingface_hub==0.19.4
RUN pip install --no-cache-dir gradio diffusers==0.30.0 pytorch-lightning==2.0.1.post0

# Copy application code
COPY . .

# Download model checkpoints
RUN mkdir -p checkpoints/mmocr checkpoints/sam checkpoints/ldm && \
    wget -q -O checkpoints/mmocr/db_swin_mix_pretrain.pth https://github.com/yeungchenwa/OCR-SAM/releases/download/ckpt/db_swin_mix_pretrain.pth && \
    wget -q -O checkpoints/mmocr/abinet_20e_st-an_mj_20221005_012617-ead8c139.pth https://download.openmmlab.com/mmocr/textrecog/abinet/abinet_20e_st-an_mj/abinet_20e_st-an_mj_20221005_012617-ead8c139.pth && \
    wget -q -O checkpoints/sam/sam_vit_h_4b8939.pth https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth && \
    wget -q -O checkpoints/ldm/last.ckpt https://heibox.uni-heidelberg.de/f/4d9ac7ea40c64582b7c9/?dl=1

# Copy model files to root directory for app.py compatibility
RUN cp checkpoints/mmocr/db_swin_mix_pretrain.pth . && \
    cp checkpoints/mmocr/abinet_20e_st-an_mj_20221005_012617-ead8c139.pth . && \
    cp checkpoints/sam/sam_vit_h_4b8939.pth . && \
    cp checkpoints/ldm/last.ckpt last.ckpt

# Expose Gradio port
EXPOSE 7860

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Launch the application
CMD ["python", "app.py"]