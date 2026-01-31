FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MAX_JOBS=4

# Create working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for model files and outputs
RUN mkdir -p pretrained_models demo/outputs inputs/applications/source_image inputs/applications/driving/densepose

# Expose Gradio port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the Gradio application
CMD ["python", "-m", "demo.gradio_animate"]