FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
ENV DA3_LOG_LEVEL=INFO
ENV DA3_WORKSPACE_DIR=gradio_workspace
ENV DA3_MODEL_DIR=depth-anything/DA3NESTED-GIANT-LARGE
ENV DA3_GALLERY_DIR=workspace/gallery
ENV CUDA_VISIBLE_DEVICES=
ENV PYTHONPATH=/home/ubuntu/deploy-projects/ea1c5487afd535cc6b3974de/src

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/ea1c5487afd535cc6b3974de

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create workspace directories
RUN mkdir -p gradio_workspace workspace/gallery

# Expose ports
EXPOSE 7860 8008

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the application
CMD ["python", "-m", "depth_anything_3.app.gradio_app", "--host", "0.0.0.0", "--port", "7860"]