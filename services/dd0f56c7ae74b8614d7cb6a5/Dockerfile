FROM python:3.6-slim

ENV PYTHONUNBUFFERED=1

# Install build dependencies and curl for healthcheck
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    python3-dev \
    curl \
    pkg-config \
    libsm6 \
    libxext6 \
    libxrender1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/dd0f56c7ae74b8614d7cb6a5

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir tensorflow==1.15.0 && \
    pip install --no-cache-dir \
    h5py==2.6.0 \
    joblib==0.9.4 \
    jsonschema==2.6.0 \
    Keras==1.2.2 \
    matplotlib==2.1.2 \
    opencv-python==3.4.0.12 \
    Pillow==3.1.2 \
    scikit-image==0.13.1 \
    scikit-learn==0.19.2 \
    scipy==1.2.3 \
    six==1.10.0 \
    flask==0.12.5

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs models skin_database

# Health check using Flask /health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run Flask web server (training runs in background)
CMD ["python", "src/web_server.py"]