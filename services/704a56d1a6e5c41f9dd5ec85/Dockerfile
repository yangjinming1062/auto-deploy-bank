FROM python:3.10-slim

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    LAZYLLM_HOME=/app/.lazyllm \
    LAZYLLM_DATA_PATH=/app/data \
    LAZYLLM_MODEL_PATH=/app/models \
    LAZYLLM_DEFAULT_LAUNCHER=empty \
    DEBIAN_FRONTEND=noninteractive

# Create necessary directories
RUN mkdir -p /app/.lazyllm /app/data /app/models /app/.temp

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.full.txt .

# Install Python dependencies in stages to handle compilation dependencies
# Install torch first as it's required by other packages like flash-attn
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir torch>=2.1.2 torchvision transformers && \
    # Install basic requirements without flash-attn first
    pip install --no-cache-dir \
        appdirs loralib toml fastapi loguru pydantic requests uvicorn \
        cloudpickle flake8 gradio gradio-client protobuf setuptools \
        docstring-parser json5 tiktoken spacy chromadb bm25s pystemmer \
        nltk jieba pyjwt sentence-transformers sentencepiece modelscope \
        psycopg2-binary sqlalchemy psutil pypdf pytest numpy pymilvus \
        async-timeout httpx rapidfuzz redis huggingface-hub pandas \
        rank-bm25 redisvl datasets deepspeed fire peft collie-lm \
        faiss-cpu google scikit-learn tensorboard tensorboard-data-server \
        vllm wandb chattts funasr lazyllm-lmdeploy timm diffusers \
        sortedcontainers lazyllm-llamafactory rotary-embedding-torch \
        lightllm infinity-emb ctranslate2 optimum typer pymongo pymysql \
        flagembedding mcp && \
    # Try to install flash-attn separately with proper torch context
    pip install --no-cache-dir flash-attn || echo "flash-attn installation failed, continuing..."

# Copy application code
COPY . .

# Install the lazyllm package
RUN pip install -e .

# Patch lightllm to work in CPU-only mode
RUN python -c "import os; \
import lightllm.models.llama.triton_kernel.context_flashattention_nopad as mod; \
orig_file = mod.__file__; \
content = open(orig_file).read(); \
content = content.replace('TESLA = \\\"Tesla\\\" in torch.cuda.get_device_name(0)', 'TESLA = False  # Force CPU mode'); \
open(orig_file, 'w').write(content); \
print('Patched lightllm for CPU mode')" 2>/dev/null || echo "Patch may have already been applied or file structure changed"

# Expose the internal port
EXPOSE 20500

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:20500/ || exit 1

# Start simple web service for testing
COPY simple_app.py /app/simple_app.py
CMD ["bash", "-lc", "python /app/simple_app.py"]