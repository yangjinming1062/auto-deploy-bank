FROM python:3.10-slim

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set Python environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy requirements and pyproject.toml first for better caching
COPY pyproject.toml requirements.txt* ./

# Install Python dependencies
# Install PyTorch first (CPU version for general use, can be overridden)
RUN pip install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install core dependencies
RUN pip install --no-cache-dir \
    diffusers \
    fairscale \
    accelerate \
    tensorboard \
    transformers \
    gradio \
    torchdiffeq \
    click \
    safetensors \
    numpy \
    soundfile \
    omegaconf \
    torchdyn \
    pytorch_lightning \
    pytorch_memlab \
    einops \
    ninja \
    torchlibrosa \
    protobuf \
    sentencepiece

# Copy the entire application code
COPY . .

# Install the package in development mode
RUN pip install -e ".[dev]"

# Expose the Gradio port (7860 is the default Gradio port)
EXPOSE 7860

# Health check - Gradio health endpoint
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the standalone demo (no model checkpoint required)
CMD ["python", "/app/demo_standalone.py"]