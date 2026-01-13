FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Copy requirements first for better caching
COPY requirements.txt .
COPY reqs_optional/ /workspace/reqs_optional/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /workspace/

# Create necessary directories
RUN mkdir -p /workspace/save /workspace/.cache/huggingface/hub

# Switch to non-root user
RUN useradd -m -u 1000 h2ogpt && \
    chown -R h2ogpt:h2ogpt /workspace
USER h2ogpt

# Expose port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the application - Gradio UI
CMD ["python", "generate.py", "--base_model=microsoft/DialoGPT-medium", "--use_safetensors=True", "--prompt_type=llama2", "--save_dir=/workspace/save/", "--use_gpu_id=False", "--score_model=None", "--max_max_new_tokens=2048", "--max_new_tokens=1024", "--gradio=True", "--share=False", "--server_name=0.0.0.0"]
