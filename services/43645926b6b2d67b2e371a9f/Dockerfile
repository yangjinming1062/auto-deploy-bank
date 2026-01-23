FROM python:3.10-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

# Install PyTorch with CUDA support
RUN pip install --no-cache-dir \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cu121

# Install core dependencies with version handling for compatibility
RUN pip install --no-cache-dir \
    transformers==4.34.0 \
    tokenizers==0.14.0 \
    accelerate==0.21.0 \
    bitsandbytes==0.40.0 \
    sentencepiece==0.1.99 \
    wandb==0.15.3

# Install remaining dependencies
RUN pip install --no-cache-dir \
    "numpy<2.0" \
    fraction \
    tqdm \
    fire \
    openai \
    scipy \
    jsonlines \
    pandas

WORKDIR /home/ubuntu/deploy-projects/43645926b6b2d67b2e371a9f

# Copy application code
COPY entrypoint.sh /entrypoint.sh
COPY train_math.py .

# Make entrypoint executable
RUN chmod +x /entrypoint.sh

# Run entrypoint script
ENTRYPOINT ["/entrypoint.sh"]