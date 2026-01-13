FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/c4625925af2d6bbe807df398

# Copy requirements first for better caching
COPY requirements.txt ./requirements_base.txt
COPY llama_adapter_v2_multimodal7b/requirements.txt ./multimodal_requirements.txt
COPY imagebind_LLM/requirements.txt ./imagebind_requirements.txt

# Create a temporary requirements file without torch
RUN grep -v "^torch" requirements_base.txt > requirements_no_torch.txt

# Install PyTorch with CUDA support
RUN pip install --no-cache-dir torch==2.0.0+cu117 torchvision==0.15.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117

# Install base requirements (without torch to avoid conflicts)
RUN pip install --no-cache-dir -r requirements_no_torch.txt

# Install additional dependencies from multimodal variant
RUN pip install --no-cache-dir \
    transformers \
    timm \
    git+https://github.com/csuhan/timm_0_3_2.git \
    git+https://github.com/openai/CLIP.git

# Install the llama package in editable mode
COPY setup.py .
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the Gradio application
CMD ["python", "start_gradio.py"]