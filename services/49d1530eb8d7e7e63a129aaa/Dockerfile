FROM python:3.10-slim

# Install curl, git for healthcheck and git dependencies
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV MASTER_ADDR=localhost
ENV MASTER_PORT=29500
ENV RANK=0
ENV LOCAL_RANK=0
ENV WORLD_SIZE=1
ENV DNNLIB_CACHE_DIR=~/.cache/dnnlib/

WORKDIR /home/ubuntu/deploy-projects/49d1530eb8d7e7e63a129aaa

# Fix numpy compatibility issue with accelerate (<2.0)
RUN pip install --no-cache-dir "numpy<2"

# Install Python dependencies first (for better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Fix gradio compatibility issue with gradio_client
RUN pip install --no-cache-dir "gradio==4.29.0" "gradio_client==0.16.1"

# Copy project code
COPY . .

# Install package in development mode
RUN python setup.py develop

EXPOSE 7860

# Healthcheck using curl
HEALTHCHECK --interval=30s --timeout=120s --start-period=300s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run gradio demo with checkpoint path from environment variable
CMD ["sh", "-c", "python demo/text_to_image_sdxl.py --checkpoint_path \"${CHECKPOINT_PATH:-/home/ubuntu/deploy-projects/49d1530eb8d7e7e63a129aaa/checkpoints/model.pt}\""]