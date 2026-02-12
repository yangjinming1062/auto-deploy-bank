FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    g++ \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender1 \
    libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DEBIAN_FRONTEND=noninteractive

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app/

# Prepare models directory and temp
RUN mkdir -p /app/models /tmp && chmod 1777 /tmp

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start the FastAPI web server with internal manga_translator instance
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]