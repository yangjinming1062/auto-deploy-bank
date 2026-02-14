FROM python:3.10-slim

# Install curl for healthcheck and OpenCV dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libgl1 \
    libglib2.0-0t64 \
    libglx0 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV HIDE_WARNING=false
ENV PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/717856b0b2e8a153a670a032

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install flash_attn stub for CPU compatibility (Florence-2 requirement)
RUN python -c "import site; print(site.getsitepackages()[0])" > /tmp/site_path.txt && \
    SITE_PATH=$(cat /tmp/site_path.txt) && \
    mkdir -p $SITE_PATH/flash_attn && \
    echo '# Stub module for flash_attn (CPU fallback)' > $SITE_PATH/flash_attn/__init__.py && \
    echo '# Stub module' > $SITE_PATH/flash_attn/bert_padding.py && \
    echo '# Stub module' > $SITE_PATH/flash_attn/flash_attn_interface.py && \
    echo 'def flash_attn_func(*args, **kwargs): raise ImportError("flash_attn not available on CPU")' >> $SITE_PATH/flash_attn/__init__.py && \
    echo 'flash_attn_varlen_func = flash_attn_func' >> $SITE_PATH/flash_attn/__init__.py

# Copy application code
COPY . .

# Create weights directory structure
RUN mkdir -p weights/icon_detect weights/icon_caption_florence

# Expose internal port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=60s --start-period=300s --retries=3 \
    CMD curl -f http://localhost:8000/probe/ || exit 1

# Start command - run the startup script that downloads models if needed
CMD ["bash", "scripts/start.sh"]