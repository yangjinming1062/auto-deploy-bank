FROM --platform=linux/amd64 python:3.8-slim
LABEL maintainer="ZJUNLP"
LABEL repository="DeepKE"

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    wget \
    git \
    curl \
    ca-certificates \
    libc6-dev \
    libstdc++-12-dev \
    libgl1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir "pip<24.1" && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn[standard] python-multipart

# Copy source code
COPY . .

# Install DeepKE package
RUN pip install --no-cache-dir -e .

# MCP dependencies already included in requirements.txt

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["uvicorn", "mcp-tools.web_server:app", "--host", "0.0.0.0", "--port", "8000"]