# Copyright (c) 2024, Xilinx/AMD Research
# FINN - Fast, Scalable Quantized Neural Network Inference on FPGAs

FROM python:3.10-slim

WORKDIR /workspace

ENV PYTHONUNBUFFERED=1 \
    FINN_ROOT=/workspace \
    FINN_BUILD_DIR=/workspace/build \
    FINN_DEPLOY_DIR=/workspace/deploy \
    RTLSIM_TRACE_DEPTH=1 \
    LIVENESS_THRESHOLD=10000 \
    PYNQ_BOARD=Pynq-Z1 \
    NETRON_PORT=8081 \
    LOCALHOST_URL=localhost

# Install curl for healthcheck
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install netron for model visualization
RUN pip install --no-cache-dir "netron>=5.0.0"

# Copy application source
COPY . .

# Install FINN in editable mode
RUN pip install --no-cache-dir -e .

# Expose internal port
EXPOSE 8081

# Healthcheck using curl
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8081/ || exit 1

# Run netron server as the main service (browse=False to avoid browser issues in container)
# Use threading to keep the server alive since netron.start() returns after starting
CMD ["python", "-c", "import netron; import threading; netron.start(None, address=('0.0.0.0', 8081), browse=False); threading.Event().wait()"]