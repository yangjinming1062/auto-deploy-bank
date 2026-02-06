FROM python:3.7-slim

WORKDIR /home/ubuntu/deploy-projects/766f570cb8ff5b694d634b2a

# Install curl for healthcheck and build dependencies for matplotlib/scipy
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    pkg-config \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    libtiff-dev \
    libwebp-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TF_CPP_MIN_LOG_LEVEL=3
ENV LOG_LEVEL=INFO
ENV CUDA_VISIBLE_DEVICES=
ENV CUDA_HOME=/usr/local/cuda

# Downgrade pip to compatible version (get_installed_distributions removed in pip 19.3)
RUN pip install --no-cache-dir pip==19.2.3

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 8080

# Health check script
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the health server
CMD ["python", "health_server.py"]