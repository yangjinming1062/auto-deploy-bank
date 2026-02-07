FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=""

WORKDIR /home/ubuntu/deploy-projects/b921526a8e06ad21a48433ff

# Install system dependencies for OpenCV and curl
# Using Debian Bookworm for compatible OpenGL libraries
RUN echo 'deb http://deb.debian.org/debian bookworm main' > /etc/apt/sources.list.d/bookworm.list && \
    apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install PyTorch CPU version and Flask
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir flask

# Copy application code
COPY . .

# Create directories for model and outputs
RUN mkdir -p /home/ubuntu/deploy-projects/b921526a8e06ad21a48433ff/outputs/model

# Expose port
EXPOSE 40209

# Default command - run Flask service
CMD ["python", "service.py"]