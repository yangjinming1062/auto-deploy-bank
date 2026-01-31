# Dockerfile for VERL (Volcano Engine Reinforcement Learning)
FROM python:3.10-slim

# Install curl for healthcheck and build essentials
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV HF_HUB_ENABLE_HF_TRANSFER=0

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/aece59c0bda9e5d51f212cc9

# Copy requirements first for better caching
COPY requirements.txt .

# Install base dependencies and specific transformers version with vision support
RUN pip install --no-cache-dir \
    "torch>=2.1.0" \
    "torchvision>=0.16.0" \
    "transformers>=4.45.0" \
    "accelerate>=0.25.0" \
    "datasets>=2.14.0" \
    "hydra-core>=1.3.0" \
    "numpy<2.0.0" \
    "pandas>=2.0.0" \
    "peft>=0.7.0" \
    "pyarrow>=19.0.0" \
    "ray[default]>=2.40.0" \
    "tensordict>=0.8.0,<=0.10.0,!=0.9.0" \
    "wandb>=0.16.0" \
    "packaging>=20.0" \
    "tensorboard>=2.14.0" \
    "uvicorn>=0.25.0" \
    "fastapi>=0.109.0" \
    "latex2sympy2_extended" \
    "math_verify" \
    "codetiming" \
    "dill" \
    "pylatexenc" \
    torchdata

# Copy application code
COPY . .

# Install the package in editable mode without dependencies
RUN pip install --no-cache-dir --no-deps -e .

# Install specific transformers version that has AutoModelForVision2Seq and AutoModelForImageTextToText
RUN pip install --no-cache-dir "transformers==4.47.0"

# Default command - will be overridden by docker-compose
CMD ["python", "-c", "import verl; print('VERL installed successfully')"]