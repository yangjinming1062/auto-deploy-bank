FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgtk-3-0 \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .
COPY pyproject.toml .

# Install CPU-only PyTorch for build (smaller size)
RUN pip install --no-cache-dir torch==2.4.0 torchvision==0.19.0 torchaudio==2.4.0 --index-url https://download.pytorch.org/whl/cpu

# Install other dependencies (excluding torch packages)
RUN pip install --no-cache-dir \
    accelerate==0.30.0 \
    torchmetrics==1.4.0 \
    tqdm==4.66.4 \
    transformers==4.40.2 \
    diffusers==0.27.2 \
    einops==0.8.0 \
    bitsandbytes==0.42 \
    scipy==1.13.0 \
    opencv-python \
    huggingface_hub==0.24.0

# Copy application source
COPY src/ ./src/
COPY __init__.py .
COPY install.py .

# Install the custom node package
RUN pip install -e .

# Clone and setup ComfyUI
RUN rm -rf /comfyui && git clone https://github.com/comfyanonymous/ComfyUI.git /comfyui

# Install ComfyUI requirements (CPU versions)
RUN cd /comfyui && pip install -r requirements.txt

# Fix dependency conflicts - ensure compatible versions
RUN pip install --no-cache-dir huggingface_hub==0.24.0 transformers==4.40.2 diffusers==0.27.2

# Create ComfyUI directory structure
RUN mkdir -p /comfyui/custom_nodes/ComfyUI-IDM-VTON

# Copy extension files to ComfyUI custom_nodes
# First create the custom node directory structure
RUN mkdir -p /comfyui/custom_nodes/ComfyUI-IDM-VTON

# Copy source code
COPY src/ /comfyui/custom_nodes/ComfyUI-IDM-VTON/src/
COPY install.py /comfyui/custom_nodes/ComfyUI-IDM-VTON/
COPY requirements.txt /comfyui/custom_nodes/ComfyUI-IDM-VTON/

# Create __init__.py that exports the mappings (combine into one RUN command)
RUN echo 'from .src.nodes_mappings import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS' > /comfyui/custom_nodes/ComfyUI-IDM-VTON/__init__.py && \
    echo '__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]' >> /comfyui/custom_nodes/ComfyUI-IDM-VTON/__init__.py

# Expose port
EXPOSE 40148

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=120s --retries=3 \
  CMD curl -f http://localhost:40148 || exit 1

# Start script that downloads models then runs ComfyUI
RUN echo '#!/bin/bash\n\
set -e\n\
cd /comfyui/custom_nodes/ComfyUI-IDM-VTON\n\
# Check if models exist in ComfyUI directory\n\
if [ ! -d "/comfyui/models/IDM-VTON" ] || [ -z "$(ls -A /comfyui/models/IDM-VTON 2>/dev/null)" ]; then\n\
  echo "=========================================="\n\
  echo "Downloading IDM-VTON model weights (~10GB)..."\n\
  echo "This may take 10-15 minutes depending on your internet connection."\n\
  echo "=========================================="\n\
  python install.py\n\
else\n\
  echo "Model weights already exist, skipping download."\n\
fi\n\
echo "=========================================="\n\
echo "Starting ComfyUI on port 40148..."\n\
echo "Access the web interface at: http://localhost:40148"\n\
echo "=========================================="\n\
cd /comfyui\n\
python main.py --listen --port 40148 --cpu\n\
' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]