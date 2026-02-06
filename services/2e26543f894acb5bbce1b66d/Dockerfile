FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/2e26543f894acb5bbce1b66d

# Set Python environment variables
ENV PYTHONUNBUFFERED=1 \
    TRANSFORMERS_OFFLINE=0 \
    TOKENIZERS_PARALLELISM=true \
    CUDA_VISIBLE_DEVICES=0 \
    TORCH_DTYPE=fp16 \
    DEFAULT_MODEL=ByteDance/Sa2VA-4B

# Copy requirements and install Python dependencies
COPY demo/requirements.txt .

# Install torch and torchvision first
RUN pip install --no-cache-dir torch==2.3.1 torchvision==0.18.1

# Install remaining dependencies
RUN pip install --no-cache-dir \
    transformers==4.42.3 \
    'opencv-python-headless<4.10' \
    'peft<0.14.0' \
    timm==1.0.9 \
    einops==0.8.0 \
    sentencepiece==0.2.0 \
    'mmengine<1' \
    gradio

# Copy the rest of the project
COPY . .

# Expose Gradio default port
EXPOSE 7860

# Run the Gradio app wrapper with default model
CMD ["python", "entrypoint.py", "ByteDance/Sa2VA-4B"]