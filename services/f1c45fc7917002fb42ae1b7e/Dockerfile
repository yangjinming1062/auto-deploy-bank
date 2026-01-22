FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=0
ENV NCCL_P2P_DISABLE=1
ENV NCCL_IB_DISABLE=1

WORKDIR /home/ubuntu/deploy-projects/f1c45fc7917002fb42ae1b7e

# Install system dependencies
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install core dependencies first
RUN pip install --no-cache-dir numpy==1.23.2

# Install PyTorch first
RUN pip install --no-cache-dir torch==2.1.0

# Install pytorch-crf (required by model.py) - version 0.7.2 supports batch_first
RUN pip install --no-cache-dir pytorch-crf==0.7.2

# Download Chinese BERT WWM model from HuggingFace
RUN pip install --no-cache-dir huggingface_hub && \
    python -c "from huggingface_hub import snapshot_download; snapshot_download('hfl/chinese-bert-wwm-ext', repo_type='model', local_dir='/home/ubuntu/deploy-projects/f1c45fc7917002fb42ae1b7e/model_hub/chinese-bert-wwm-ext')"

# Install remaining dependencies (skip CUDA-dependent packages for CPU-only environment)
# Reinstall numpy at the end to ensure correct version (PyTorch 2.1.0 requires NumPy < 2)
RUN sed -i '/^torch==/d; /^numpy==/d; /^flash-attn==/d; /^deepspeed==/d; /^bitsandbytes==/d; /^torchcrf==/d' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir numpy==1.23.2 --force-reinstall

# Copy application code
COPY . .

EXPOSE 8080

CMD ["python", "app.py"]