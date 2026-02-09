FROM python:3.8-slim

# Install system dependencies for audio processing and healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/37e8503f9f8861a8e6385b1e

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create required directories
RUN mkdir -p logs models

# Default command - training script
# Web service command: python app.py
CMD ["python", "train.py"]