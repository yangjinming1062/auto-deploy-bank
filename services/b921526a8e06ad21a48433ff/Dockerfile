FROM python:3.7-slim

# Install curl for healthcheck, build-essential for pycocotools, and OpenCV dependencies
RUN apt-get update && apt-get install -y curl build-essential libglib2.0-0 libgtk2.0-0 libnotify-dev libgstreamer1.0-0 libgstreamer-plugins-base1.0-0 && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CUDA_HOME=/usr/local/cuda
ENV FORCE_CUDA=0
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/b921526a8e06ad21a48433ff

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
# Install PyTorch CPU version since FORCE_CUDA=0
# Cython is required for pycocotools, install it first
RUN pip install --no-cache-dir Cython && \
    pip install --no-cache-dir torch torchvision torchaudio -f https://download.pytorch.org/whl/cpu/torch_stable.html && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pyyaml termcolor

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/model data/record data/result && chmod +x start.sh

# Healthcheck - verify the training process is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD pgrep -f "python.*train_net" > /dev/null || exit 1

# Default command - run training (task is defined in config file)
CMD ["./start.sh", "--cfg_file", "configs/city_snake.yaml"]