FROM python:3.9-slim

WORKDIR /home/user

# Install curl for healthcheck and build dependencies for pi-heif
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    libheif-dev \
    libde265-dev \
    libx265-dev \
    libjpeg-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Create symlink for pi-heif to find libheif headers
RUN if [ -d /usr/include/x86_64-linux-gnu/libheif ]; then \
        ln -sf /usr/include/x86_64-linux-gnu/libheif /usr/include/libheif; \
    fi

# Install nebula-graph for knowledge graph functionality
RUN wget -q https://oss-cdn.nebula-graph.com.cn/package/3.6.0/nebula-graph-3.6.0.ubuntu1804.amd64.deb && \
    dpkg -i nebula-graph-3.6.0.ubuntu1804.amd64.deb 2>/dev/null || true && \
    rm -f nebula-graph-3.6.0.ubuntu1804.amd64.deb

# Set Python environment variables
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy and install dependencies
COPY requirements.txt .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt || \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Setup config files from examples
RUN cp /home/user/configs/model_config.py.example /home/user/configs/model_config.py && \
    cp /home/user/configs/server_config.py.example /home/user/configs/server_config.py && \
    # Set DEFAULT_BIND_HOST to 0.0.0.0 for container access
    sed -i 's/DEFAULT_BIND_HOST = "127.0.0.1"/DEFAULT_BIND_HOST = "0.0.0.0"/g' /home/user/configs/server_config.py && \
    # Set NO_REMOTE_API to False to enable local API
    sed -i 's/NO_REMOTE_API = True/NO_REMOTE_API = False/g' /home/user/configs/server_config.py && \
    # Set DOCKER_SERVICE to False to run services directly
    sed -i 's/DOCKER_SERVICE = True/DOCKER_SERVICE = False/g' /home/user/configs/server_config.py && \
    # Set SANDBOX_DO_REMOTE to False for local sandbox
    sed -i 's/SANDBOX_DO_REMOTE = True/SANDBOX_DO_REMOTE = False/g' /home/user/configs/server_config.py

# Create necessary directories
RUN mkdir -p /home/user/logs /home/user/jupyter_work /home/user/data/nebula_data

# Expose main service port (Streamlit web UI)
EXPOSE 8501

# Health check - check Streamlit UI
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Start the application
CMD ["bash", "-c", "/home/user/scripts/start.sh"]