FROM python:3.8-slim

LABEL maintainer="DeepKE Team"
LABEL repository="DeepKE"
LABEL description="DeepKE Knowledge Extraction API"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV CUDA_VISIBLE_DEVICES=0
ENV CUDA_DEVICE_ORDER=PCI_BUS_ID
ENV TOKENIZERS_PARALLELISM=false
ENV WANDB_DISABLED=true
ENV WANDB_API_KEY=
ENV MASTER_PORT=29500
ENV DEEPKE_PATH=/home/ubuntu/deploy-projects/9f875d92ad32d30b7fbad152
ENV PYTHONPATH=$PYTHONPATH:/home/ubuntu/deploy-projects/9f875d92ad32d30b7fbad152

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
    linux-libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Create conda environment for DeepKE
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-4.7.12-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

ENV PATH=/opt/conda/bin:$PATH

# Create DeepKE environment
RUN conda create -y --name deepke python=3.8 && \
    conda create -y --name deepke-ee python=3.8

# Set conda paths
ENV CONDA_PY=/opt/conda/envs/deepke/bin/python
ENV CONDA_EE_PY=/opt/conda/envs/deepke-ee/bin/python
ENV CONDA_DEFAULT_ENV=deepke

# Copy requirements file
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies in main environment
RUN pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn[standard] python-multipart

# Install DeepKE in deepke environment
RUN /bin/bash -c "source /opt/conda/bin/activate deepke && pip install --no-cache-dir -r /tmp/requirements.txt && pip install --no-cache-dir setuptools_scm && pip install -e ."

# Install DeepKE in deepke-ee environment
RUN /bin/bash -c "source /opt/conda/bin/activate deepke-ee && pip install --no-cache-dir -r /tmp/requirements.txt && pip install --no-cache-dir setuptools_scm && pip install -e ."

# Copy application code
WORKDIR /home/ubuntu/deploy-projects/9f875d92ad32d30b7fbad152
COPY api_server.py /home/ubuntu/deploy-projects/9f875d92ad32d30b7fbad152/
COPY mcp-tools/ /home/ubuntu/deploy-projects/9f875d92ad32d30b7fbad152/mcp-tools/
COPY src/ /home/ubuntu/deploy-projects/9f875d92ad32d30b7fbad_image/src/
COPY example/ /home/ubuntu/deploy-projects/9f875d92ad32d30b7fbad_image/example/

# Expose port
EXPOSE 40181

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:40181/health || exit 1

# Start the API server
CMD ["python", "api_server.py"]