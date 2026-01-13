FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    make \
    cmake \
    libc6-dev \
    libopenmpi-dev \
    default-jre-headless \
    git \
    wget \
    pkg-config \
    libboost-all-dev \
    libgoogle-glog-dev \
    protobuf-compiler \
    libprotobuf-dev \
    libyaml-cpp-dev \
    rapidjson-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GRAPHSCOPE_HOME=/opt/graphscope
ENV INSTALL_PREFIX=/opt/graphscope
ENV GRAPHSCOPE_DEBUG=false
ENV GRAPHSCOPE_RUNTIME=~/.graphscope/runtime/coordinator
ENV GSCONFIG=~/.gsctl
ENV GS_GRPC_CHUNK_SIZE=268435455
ENV VINEYARD_USE_LOCAL_REGISTRY=TRUE
ENV WITHOUT_LEARNING_ENGINE=
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
ENV GRPC_ENABLE_FORK_SUPPORT=false
ENV CLUSTER_TYPE=HOSTS
ENV NAMESPACE=kubetask
ENV INSTANCE_NAME=demo

# Set working directory
WORKDIR /app

# Copy Python requirements first for better caching
COPY python/requirements.txt ./python_requirements.txt
COPY coordinator/requirements.txt ./coordinator_requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r python_requirements.txt && \
    pip install --no-cache-dir -r coordinator_requirements.txt

# Copy application code
COPY . .

# Copy VERSION file to coordinator and python directories for version detection
RUN cp /app/VERSION /app/coordinator/gscoordinator/VERSION && \
    cp /app/VERSION /app/python/graphscope/VERSION

# Install Python packages first, then coordinator
RUN pip install --no-cache-dir -e python/ && \
    pip install --no-cache-dir -e coordinator/

# Expose the HTTP service port (8080) and gRPC service port (63800)
EXPOSE 8080 63800

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Start the coordinator service
CMD ["python", "-m", "gscoordinator.coordinator", "--config-file", "config.yaml"]