FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    TOKENIZERS_PARALLELISM=false \
    CUDA_HOME=/usr/local/cuda \
    PATH="$CUDA_HOME/bin:$PATH"

# Install curl for healthcheck and system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Copy requirements first for better layer caching
COPY requirements.txt /workspace/requirements.txt

# Install pytorch with CUDA
RUN pip install --no-cache-dir torch==2.5.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install Python dependencies (flash-attn skipped as it requires full CUDA toolkit)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn && \
    pip install --no-cache-dir "cog>=0.12.0" && \
    pip install --no-cache-dir opencv-fixer==0.2.5 && \
    python -c "from opencv_fixer import AutoFix; AutoFix()"

# Install pget for downloading model weights
RUN curl -o /usr/local/bin/pget -L "https://github.com/replicate/pget/releases/download/v0.6.0/pget_linux_x86_64" && chmod +x /usr/local/bin/pget

# Copy application code
COPY . .

# Set environment variables from conf.py
ENV HF_TOKEN="[YOUR HF_TOKEN]"
ENV HF_HOME="[YOUR HF_HOME]"
ENV GPT_AK="[YOUR GPT_AK]"
ENV WORLD_SIZE=""

EXPOSE 8000

CMD ["python", "server.py"]