FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects

# Copy requirements and install Python dependencies
COPY requirements.txt .

# Upgrade pip and install packaging first
RUN pip install --no-cache-dir --upgrade pip packaging

# Install torch first (needed for flash-attn)
RUN pip install --no-cache-dir "torch>=2.0.0"

# Install remaining dependencies excluding flash-attn and deepspeed
RUN pip install --no-cache-dir \
    safetensors==0.3.1 \
    datasets==2.10.1 \
    accelerate>=0.20.3 \
    protobuf==3.20.2 \
    transformers>=4.34.0 \
    scikit-learn==1.0.2 \
    evaluate==0.4.0 \
    texttable==1.6.7 \
    toml==0.10.2 \
    numpy>=1.22.0 \
    sentencepiece==0.1.98 \
    fire==0.5.0 \
    streamlit==1.24.1

# Install deepspeed (skip flash-attn as it requires nvcc)
RUN pip install --no-cache-dir deepspeed==0.9.5

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TOKENIZERS_PARALLELISM=false
ENV WANDB_DISABLED=true
ENV CUDA_VISIBLE_DEVICES=0
ENV HF_MODEL_HUB=""

# Expose Streamlit port
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "apps/web_demo.py", "--", "--model_path=tigerbot-13b-chat"]