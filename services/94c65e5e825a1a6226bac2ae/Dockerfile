# VeOmni ML Framework Service Dockerfile
FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Define environments
ENV PYTHONUNBUFFERED=1
ENV CACHE_DIR=~/.cache/veomni
ENV VEOMNI_VERBOSITY=warn
ENV MODELING_BACKEND=hf
ENV USE_LIGER_KERNEL=0
ENV DISABLE_WARNINGS=0
ENV INTERNAL_PORT=8000

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/94c65e5e825a1a6226bac2ae

# Install uv for fast package management
COPY --from=ghcr.io/astral-sh/uv:0.9.8 /uv /bin/uv
ENV PATH="/bin:$PATH"
ENV UV_CACHE_DIR=/root/.cache/uv

# Copy source files needed for build
COPY pyproject.toml uv.lock ./
COPY veomni ./veomni
COPY service.py .

# Upgrade pip first
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install dependencies (using && to chain commands properly)
RUN pip install --no-cache-dir \
    "transformers==4.57.3" \
    "diffusers>=0.30.0,<=0.31.0" \
    "datasets>=2.16.0,<=2.21.0" \
    "einops>=0.8.1" \
    timm \
    wandb \
    "blobfile>=3.0.0" \
    "torchdata>=0.8.0,<1.0" \
    "tiktoken>=0.9.0" \
    psutil \
    setuptools

# Install the package in editable mode
RUN pip install --no-cache-dir -e .

# Copy remaining source
COPY tasks ./tasks

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the service
CMD ["python", "service.py"]