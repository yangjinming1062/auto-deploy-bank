FROM python:3.8-slim

# Install curl and build essentials for compiling pycocotools
# Also install OpenCV runtime dependencies
RUN apt-get update && apt-get install -y curl gcc g++ build-essential libglib2.0-0 libsm6 libxext6 libxrender1 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/b921526a8e06ad21a48433ff

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install PyTorch and dependencies (CPU version for building)
# For GPU training, use: pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install Cython for pycocotools build
RUN pip install Cython

# Install compatible protobuf version for tensorboardX
RUN pip install 'protobuf>=3.8.0,<3.20.0' termcolor

# Copy and install Python dependencies
COPY requirements.txt .
# Update to compatible versions for Python 3.8
RUN sed -i 's/opencv-contrib-python==3.4.2.17/opencv-contrib-python==3.4.8.29/g' requirements.txt && \
    sed -i 's/opencv-python==3.4.2.17/opencv-python==3.4.8.29/g' requirements.txt && \
    sed -i 's/numpy==1.16.4/numpy>=1.16.0/g' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Build CUDA extensions (requires GPU and CUDA toolkit)
# Skip this step in CPU-only environment - for GPU training, uncomment and run with nvidia-docker:
# RUN cd lib/csrc/dcn_v2 && python setup.py build_ext --inplace && \
#     cd ../extreme_utils && python setup.py build_ext --inplace && \
#     cd ../roi_align_layer && python setup.py build_ext --inplace

# Make healthcheck script executable
RUN chmod +x /home/ubuntu/deploy-projects/b921526a8e06ad21a48433ff/healthcheck_server.py

# Default command - start healthcheck server (use: docker compose run deep-snake python train_net.py ... for training)
CMD ["python", "healthcheck_server.py"]