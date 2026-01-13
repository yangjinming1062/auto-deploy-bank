FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    python3-dev \
    cmake \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TORCH_SHARE_STRATEGY=file_system
ENV OMP_NUM_THREADS=1

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements_3090.txt requirements_3090.txt

# Install PyTorch first
RUN pip install --no-cache-dir torch==1.10.0

# Install remaining dependencies
RUN pip install --no-cache-dir -r requirements_3090.txt

# Copy the rest of the codebase
COPY . .

# Expose Gradio port (default is 7860)
EXPOSE 7860

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the Gradio demo interface (doesn't require model checkpoints)
CMD ["python", "inference/svs/gradio/demo.py"]