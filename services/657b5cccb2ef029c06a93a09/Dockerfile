# 3DTrajMaster Gradio Web Service
FROM python:3.10-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip first
RUN pip install --no-cache-dir pip==25.3

# Install Python dependencies
COPY CogVideo/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/657b5cccb2ef029c06a93a09

# Copy application code
COPY CogVideo/ ./CogVideo/
COPY dataset/ ./dataset/
COPY eval/ ./eval/

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Expose gradio port
EXPOSE 7860

# Default command - launch gradio interface
CMD ["python", "CogVideo/tools/llm_flux_cogvideox/gradio_page.py"]