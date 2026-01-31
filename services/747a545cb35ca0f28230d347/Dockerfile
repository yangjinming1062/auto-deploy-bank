FROM python:3.8-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    YOLOX_DATADIR="" \
    NCCL_LAUNCH_MODE="PARALLEL" \
    NCCL_IB_GID_INDEX="3" \
    NCCL_IB_TC="106" \
    OPENCV_OPENCL_RUNTIME="disabled"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    pkg-config \
    cmake \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/747a545cb35ca0f28230d347

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Build C++ extensions and install package
RUN python3 setup.py develop

# Expose the port
EXPOSE 46685

# Run Flask web server
CMD ["python3", "web_server.py"]