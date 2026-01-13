FROM ubuntu:22.04

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    python3.10 \
    python3.10-dev \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgtk-3-0 \
    libegl1-mesa \
    libx11-6 \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set python3 as default python
RUN ln -sf /usr/bin/python3.10 /usr/bin/python

# Install pip
RUN python -m pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TOKENIZERS_PARALLELISM=false
ENV FLUX_SCHNELL=
ENV AE=
ENV ENV_TYPE=
ENV RoPE=
ENV PL_GLOBAL_SEED=42
ENV TRANSFORMERS_CACHE=/tmp/transformers_cache
ENV HF_HOME=/tmp/hf_home

# Make startup script executable
RUN chmod +x start.sh

# Expose port
EXPOSE 7860

# Run the application
CMD ["./start.sh"]