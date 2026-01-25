FROM python:3.9-slim

# Install system dependencies for TensorFlow, OpenCV, and GUI support
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    libgl1 \
    libglx-mesa0 \
    libglapi-mesa \
    libglib2.0-0 \
    libxcb1 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libsm6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/13b8566b939feb4c5f4b2f55

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DNNLIB_CACHE_DIR=/home/ubuntu/deploy-projects/13b8566b939feb4c5f4b2f55/.cache/dnnlib \
    PORT=29500 \
    MASTER_PORT=29500

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p checkpoints work_dirs data

# Default command - synthesize with a demo model (user can override)
CMD ["python", "synthesize.py", "stylegan_demo"]