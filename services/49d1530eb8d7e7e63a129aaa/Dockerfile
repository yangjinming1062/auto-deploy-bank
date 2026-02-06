FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=0
ENV PYTHONPATH=/home/ubuntu/deploy-projects/49d1530eb8d7e7e63a129aaa

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/49d1530eb8d7e7e63a129aaa

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Gradio default port
EXPOSE 7860

# Healthcheck
HEALTHCHECK --interval=30s --timeout=60s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the Gradio demo app
CMD ["python", "start_app.py"]