FROM python:3.10-slim

# Install system dependencies including ffmpeg (required by the package)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    git \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    HF_CACHE_DIR=/home/appuser/hf_cache \
    HF_HOME=/home/appuser/hf_cache \
    TORCH_HOME=/home/appuser/torch_cache \
    TOKENIZERS_PARALLELISM=false \
    PORT=40424

# Create non-root user
RUN useradd -m -s /bin/bash appuser && \
    mkdir -p /home/appuser/hf_cache /home/appuser/torch_cache && \
    chown -R appuser:appuser /home/appuser/hf_cache /home/appuser/torch_cache

# Set working directory
WORKDIR /home/appuser

# Copy requirements first for better layer caching
COPY --chown=appuser:appuser pyproject.toml ./

# Install dependencies using pip install -e . from pyproject.toml
RUN pip install --no-cache-dir -e . 2>&1 | tail -30

# Install FastAPI and uvicorn
RUN pip install --no-cache-dir fastapi uvicorn 2>&1 | tail -5

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose the service port
EXPOSE 40424

# Default command - run the FastAPI server
CMD ["python", "server.py"]