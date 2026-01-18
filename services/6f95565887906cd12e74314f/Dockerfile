FROM python:3.10-slim

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONPATH=/home/ubuntu/deploy-projects/6f95565887906cd12e74314f

# Install CUDA-enabled PyTorch (matching CLAUDE.md requirements)
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/6f95565887906cd12e74314f

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Clone and install taming-transformers
RUN git clone --depth 1 https://github.com/CompVis/taming-transformers.git /tmp/taming-transformers && \
    pip install -e /tmp/taming-transformers && \
    rm -rf /tmp/taming-transformers

# Copy application code
COPY . .

# Expose port (Flask default)
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the healthcheck service
CMD ["python", "service.py"]