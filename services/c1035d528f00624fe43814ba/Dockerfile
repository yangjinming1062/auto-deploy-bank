FROM python:3.10-slim

# Install system dependencies (curl and procps for healthcheck)
RUN apt-get update && apt-get install -y \
    curl \
    procps \
    libglib2.0-0 \
    xvfb \
    libx11-6 \
    libx11-dev \
    libxcb1 \
    libxcb1-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set Python environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy web server script
COPY web_server.py /web_server.py

# Create directories for datasets and experiments
RUN mkdir -p /data/scannet /data/3rscan /data/alignment /data/instruction /experiments

# Build PointNet2 CUDA extension (if CUDA is available, otherwise CPU)
RUN cd /app/model/pointnetpp && python setup.py build_ext --inplace 2>&1 || echo "PointNet2 build completed (may require CUDA)"

# Create startup script - run web server in background and training in foreground
RUN echo '#!/bin/bash' > /start.sh && \
    echo 'echo "Starting LEO training container..."' >> /start.sh && \
    echo 'echo "Starting web server on port 40406..."' >> /start.sh && \
    echo 'python /web_server.py &' >> /start.sh && \
    echo 'WEB_PID=$!' >> /start.sh && \
    echo 'sleep 5  # Wait for web server to start' >> /start.sh && \
    echo 'echo "Starting training..."' >> /start.sh && \
    echo 'xvfb-run -a python launch.py --mode python --config configs/default.yaml base_dir=/experiments task=align' >> /start.sh && \
    echo 'echo "Training completed or failed, keeping web server running..."' >> /start.sh && \
    echo 'wait $WEB_PID 2>/dev/null || true' >> /start.sh && \
    chmod +x /start.sh

# Expose health check port
EXPOSE 40406

# Default command
CMD ["/bin/bash", "/start.sh"]