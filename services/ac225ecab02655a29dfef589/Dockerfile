FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    xvfb \
    x11-utils \
    libgl1 \
    libglib2.0-0 \
    libxcb1 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY PC-Agent/requirements-docker.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install additional Python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    python-multipart \
    pydantic \
    qwen_agent \
    qwen_vl_utils \
    adb-shell \
    vllm \
    transformers

# Copy application code
COPY PC-Agent/ ./PC-Agent/
COPY . .

# Create directories for screenshots
RUN mkdir -p /app/task_1 /app/temp

# Copy entrypoint script
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port
EXPOSE 40513

# Set environment variables
ENV DISPLAY=:99
ENV QT_QPA_PLATFORM=offscreen
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:40513/health || exit 1

# Start command
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "web_api:app", "--host", "0.0.0.0", "--port", "40513"]