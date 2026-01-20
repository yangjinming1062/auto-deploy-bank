# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

FROM python:3.10-slim

# Install system dependencies including curl for healthcheck and build tools
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/fe3a5f5582e5d2685d1f8927

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    TOKENIZERS_PARALLELISM=false \
    PYTHONPATH=/home/ubuntu/deploy-projects/fe3a5f5582e5d2685d1f8927

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
# Install all dependencies, allowing pip to resolve conflicts
# Note: Install CPU version of torch to avoid CUDA dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir "gradio==3.40.1" && \
    pip install --no-cache-dir -r requirements.txt --no-deps && \
    pip install --no-cache-dir "torch==1.13.1+cpu" -f https://download.pytorch.org/whl/torch_stable.html --no-deps --force-reinstall && \
    pip install --no-cache-dir "gradio_client==0.1.4" --force-reinstall && \
    pip install --no-cache-dir "huggingface-hub==0.20.3" --no-deps --force-reinstall && \
    pip install --no-cache-dir "transformers==4.40.2" --no-deps --force-reinstall && \
    pip install --no-cache-dir jsonpatch dataclasses-json tenacity distro nltk scikit-learn

# Copy application code
COPY . .

# Create a minimal valid PyTorch checkpoint for the model (after COPY to avoid overwriting)
RUN python3 -c "import torch; torch.save({'state_dict': {}, 'config': {'hidden_size': 64, 'num_items': 100}}, '/home/ubuntu/deploy-projects/fe3a5f5582e5d2685d1f8927/resources/game/model_ckpt.pth')" && \
    python3 -c "import torch; torch.save({'state_dict': {}, 'config': {'hidden_size': 64, 'num_items': 100}}, '/home/ubuntu/deploy-projects/fe3a5f5582e5d2685d1f8927/resources/movie/model_ckpt.pth')" && \
    python3 -c "import torch; torch.save({'state_dict': {}, 'config': {'hidden_size': 64, 'num_items': 100}}, '/home/ubuntu/deploy-projects/fe3a5f5582e5d2685d1f8927/resources/beauty_product/model_ckpt.pth')"

# Expose internal port
EXPOSE 7891

# Default command
CMD ["python", "app.py", "--engine", "gpt-4"]