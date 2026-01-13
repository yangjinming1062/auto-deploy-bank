FROM python:3.8-slim

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create working directory
WORKDIR /workspace

# Copy requirements files
COPY dev-requirements.txt .
COPY sdk/python/dev-requirements.txt ./sdk-python-requirements.txt
COPY sdk/python/mlflow-requirements.txt ./mlflow-requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r dev-requirements.txt && \
    pip install -r sdk-python-requirements.txt && \
    pip install -r mlflow-requirements.txt && \
    pip install azure-ai-ml && \
    pip install mldesigner mltable && \
    pip install "protobuf<=5.28.3" && \
    pip install jupyterlab && \
    rm dev-requirements.txt sdk-python-requirements.txt mlflow-requirements.txt

# Copy repository contents
COPY . .

# Expose Jupyter port
EXPOSE 8888

# Copy Jupyter configuration
COPY .devcontainer/jupyter_server_config.py /root/.jupyter/jupyter_server_config.py

# Set startup command
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--ServerApp.token=''", "--ServerApp.password=''", "--ServerApp.allow_origin='*'"]