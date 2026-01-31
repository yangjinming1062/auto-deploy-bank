FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl ffmpeg libgl1 libsm6 libxext6 libxrender-dev build-essential && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV RANK=0
ENV XDG_CACHE_HOME=/root/.cache
ENV TOKENIZERS_PARALLELISM=false

WORKDIR /home/ubuntu/deploy-projects/bd1e5b31a122714865387604

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create temp directory for outputs
RUN mkdir -p temp && chmod 777 temp

# Expose the Gradio port
EXPOSE 7860

# Run the application
CMD ["python", "gradio_app.py"]