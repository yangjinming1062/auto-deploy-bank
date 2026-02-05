FROM python:3.11-slim

# Install system dependencies for PyQt5 and other packages
RUN apt-get update && apt-get install -y \
    curl \
    libgl1 \
    libglib2.0-0 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/ac27575ebeeea064f8dfabab

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    OMP_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1 \
    VECLIB_MAXIMUM_THREADS=1 \
    NUMEXPR_NUM_THREADS=1 \
    TOKENIZERS_PARALLELISM=false \
    PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 \
    PYTORCH_ENABLE_MPS_FALLBACK=1

# Copy requirements first for better cache
COPY server-requirements.txt .

# Install dependencies in batches to avoid blocking on optional deps
# First install core packages that don't have problematic optional deps
RUN pip install --no-cache-dir \
    uvicorn>=0.27.0 \
    fastapi>=0.109.0 \
    pydantic>=2.5.0 \
    httpx>=0.26.0 \
    json5>=0.9.0 \
    pydub>=0.25.1 \
    dashscope>=1.25.3 \
    paho-mqtt>=2.1.0 \
    markdown>=3.10 \
    flask>=3.0.0 \
    mcp>=1.0.0 \
    openai>=1.0.0 \
    requests>=2.31.0 \
    aiohttp>=3.9.0 \
    python-dotenv>=1.0.0 \
    psutil>=5.9.0 \
    gevent>=23.0.0 \
    PyQt5>=5.15.0 \
    && pip install --no-cache-dir --no-deps nagaagent-core>=1.0.9 || true

# Copy application code
COPY . .

# Create entry point script
RUN chmod +x /home/ubuntu/deploy-projects/ac27575ebeeea064f8dfabab/scripts/docker-entrypoint.sh

EXPOSE 8000 8001 8003

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start all servers
CMD ["/home/ubuntu/deploy-projects/ac27575ebeeea064f8dfabab/scripts/docker-entrypoint.sh"]