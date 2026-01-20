# Root-level Dockerfile for InteRecAgent
# Builds the application from the InteRecAgent subdirectory

FROM python:3.10-slim

# Install system dependencies including curl for healthcheck and build tools
RUN apt-get update && apt-get install -y curl build-essential git && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/fe3a5f5582e5d2685d1f8927

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    TOKENIZERS_PARALLELISM=false \
    PYTHONPATH=/home/ubuntu/deploy-projects/fe3a5f5582e5d2685d1f8927

# Copy requirements first for better caching
COPY InteRecAgent/requirements.txt .

# Upgrade pip and install Python dependencies
# Install specific pinned versions to avoid dependency conflicts
# Use older setuptools to avoid cython_sources issue with pyyaml
RUN pip install --no-cache-dir --upgrade pip "setuptools<70.0.0" wheel && \
    # Install torch CPU-only first
    pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu "torch==1.13.1" && \
    # Pin specific versions of core dependencies that have strict requirements
    # huggingface-hub 0.23.0+ has split_torch_state_dict_into_shards needed by transformers 4.40+
    # tokenizers 0.19.x works with transformers 4.40.2
    pip install --no-cache-dir "tokenizers==0.19.0" --no-deps && \
    pip install --no-cache-dir "huggingface-hub==0.23.0" --no-deps && \
    pip install --no-cache-dir "gradio==3.40.1" && \
    pip install --no-cache-dir -r requirements.txt --no-deps && \
    pip install --no-cache-dir "gradio_client==0.1.4" --force-reinstall && \
    pip install --no-cache-dir "websockets>=10.0,<12.0" --force-reinstall && \
    pip install --no-cache-dir langsmith sniffio distro tenacity jsonpatch==1.33 mypy_extensions==0.4.4 nltk==3.8.1 safetensors>=0.4.1 "scikit-learn>=1.2.0" && \
    # Clone and install UniRec from GitHub
    git clone --depth 1 https://github.com/microsoft/UniRec.git /tmp/unirec && \
    cd /tmp/unirec && \
    pip install --no-cache-dir --user --upgrade setuptools wheel twine && \
    python setup.py sdist bdist_wheel 2>/dev/null || python setup.py bdist_wheel && \
    pip install --no-cache-dir dist/unirec-*.whl && \
    cd / && rm -rf /tmp/unirec && \
    # Reinstall transformers with compatible tokenizers and huggingface-hub
    pip install --no-cache-dir "transformers==4.40.2" --no-deps --force-reinstall && \
    # Additional dependencies for chromadb (pydantic-settings for pydantic v2 compatibility)
    # Use chromadb 0.4.15 which is compatible with langchain 0.0.312
    pip install --no-cache-dir overrides>=7.3.1 posthog>=2.4.0 bcrypt>=4.0.1 pydantic-settings "chromadb==0.4.15" && \
    # Pin numpy to compatible version for pandas <2.1.0
    pip install --no-cache-dir "numpy<1.29.0" --force-reinstall && \
    # Install sentencepiece for sentence_transformers 2.2.2
    pip install --no-cache-dir sentencepiece --force-reinstall && \
    # Re-pin core dependencies in case they were upgraded
    pip install --no-cache-dir "tokenizers==0.19.0" --no-deps --force-reinstall && \
    pip install --no-cache-dir "huggingface-hub==0.23.0" --no-deps --force-reinstall

# Copy application code
COPY InteRecAgent/ .

# Patch the ranking tool to work without a real model for demo purposes
COPY patch_ranking.py /tmp/patch_ranking.py
RUN python3 /tmp/patch_ranking.py

# Create minimal valid PyTorch checkpoints for the model
RUN mkdir -p resources/game resources/movie resources/beauty_product && \
    python3 -c "import torch; ckpt={'state_dict':{},'config':{'model':'MF'}}; torch.save(ckpt,'resources/game/model_ckpt.pth'); torch.save(ckpt,'resources/movie/model_ckpt.pth'); torch.save(ckpt,'resources/beauty_product/model_ckpt.pth')"

# Expose internal port
EXPOSE 7891

# Default command
CMD ["python", "app.py", "--engine", "gpt-4"]