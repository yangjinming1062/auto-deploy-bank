FROM python:3.7-slim

# Install curl, build essentials, and libsndfile for audio processing
RUN apt-get update && apt-get install -y curl gcc g++ libsndfile1 && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TF_CPP_MIN_LOG_LEVEL=1

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/5b7a5be3bb6a00daea517b54

# Copy requirements first for better caching
COPY requirements.txt .

# Install numpy and Cython first (required by some packages during build)
RUN pip install --no-cache-dir numpy==1.16.4 Cython

# Downgrade protobuf for TF 1.13 compatibility
RUN pip install --no-cache-dir protobuf==3.20.3

# Install remaining Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for models and outputs
RUN mkdir -p /home/ubuntu/deploy-projects/5b7a5be3bb6a00daea517b54/synthesizer/saved_models

# Healthcheck - check if Python is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:40721/ || exit 1

# Default command - run Flask API
CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "40721"]