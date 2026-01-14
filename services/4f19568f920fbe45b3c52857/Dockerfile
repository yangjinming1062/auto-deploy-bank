# AI Glass System - Dockerfile
# Computer vision application (CPU-only mode, headless)

FROM python:3.10-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    portaudio19-dev \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libgomp1 \
    git \
    wget \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Copy requirements.txt first for better layer caching
COPY requirements.txt .

# Install PyTorch (CPU-only version for non-GPU environments)
RUN pip install torch==2.0.1 --index-url https://download.pytorch.org/whl/cpu
RUN pip install torchvision==0.15.2 --index-url https://download.pytorch.org/whl/cpu

# Install remaining Python dependencies
# Note: Replace opencv-python with opencv-python-headless for headless environments
RUN sed -i 's/opencv-python==4.8.1.78/opencv-python-headless==4.8.1.78/g' requirements.txt
RUN sed -i 's/opencv-contrib-python==4.8.1.78/opencv-python-headless==4.8.1.78/g' requirements.txt
RUN grep -v '^torch\|^torchvision\|^opencv' requirements.txt > requirements_temp.txt && \
    pip install --no-cache-dir -r requirements_temp.txt && \
    rm requirements_temp.txt

# Fix httpx version compatibility with openai 1.3.5 (httpx<0.26.0 required)
RUN pip install --no-cache-dir 'httpx<0.26.0'

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p recordings model music voice static templates

# Expose ports
EXPOSE 8081 12345/udp

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8081/api/health || exit 1

# Start command
CMD ["python3", "app_main.py"]