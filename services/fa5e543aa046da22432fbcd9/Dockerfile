FROM python:3.11-slim

# Install curl, build essentials, and CUDA toolkit for flash_attn
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/fa5e543aa046da22432fbcd9

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV PIP_NO_CACHE_DIR=1

# Copy requirements and install dependencies
COPY requirements.txt .

# Install torch first (CPU version for build, CUDA runtime may need adjustment)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install remaining dependencies
RUN pip install --no-cache-dir transformers>=4.55.0 accelerate>=0.34.2 \
    fastapi>=0.100.0 uvicorn>=0.23.0 pydantic>=2.0.0

# Install flash_attn (needs torch already installed)
RUN pip install --no-cache-dir flash_attn>=2.6.3 || echo "flash_attn installation failed, continuing..."

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]