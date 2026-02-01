FROM python:3.10-slim

# Install system dependencies including ffmpeg for imageio-ffmpeg, curl for healthcheck, and wget for downloads
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/c2fd5dc4b6693f444ea2903f

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Download model checkpoints
RUN chmod +x get_weights.sh && ./get_weights.sh

# Expose Gradio default port
EXPOSE 7860

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the Gradio application
CMD ["python", "app.py"]