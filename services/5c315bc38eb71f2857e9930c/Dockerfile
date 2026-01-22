FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CUDA_DEVICE_ORDER=PCI_BUS_ID \
    HF_HOME=/root/.cache/huggingface

WORKDIR /home/ubuntu/deploy-projects/5c315bc38eb71f2857e9930c

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    wget \
    python3.10 \
    python3.10-dev \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install kiui package
RUN pip install --no-cache-dir kiui==0.3.1

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p outputs/V3D_512 && mkdir -p ckpts

# Expose port
EXPOSE 4321

# Health check
HEALTHCHECK --interval=60s --timeout=30s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:4321/ || exit 1

# Start the application
CMD ["python3", "app.py", "--port", "4321", "--host", "0.0.0.0", "--device", "cuda"]