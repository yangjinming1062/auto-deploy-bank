FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1 \
    CUDA_DEVICE_ORDER=PCI_BUS_ID \
    CUDA_VISIBLE_DEVICES=0

WORKDIR /home/ubuntu/deploy-projects/47bb5f3ab9460c0e249214c4

# Install curl for healthcheck and OpenCV dependencies
RUN apt-get update && apt-get install -y curl libglib2.0-0 libsm6 libxext6 libxrender1 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
# Filter out problematic packages, update numpy, and install thop separately
RUN sed -i 's/numpy==1.17.0/numpy==1.18.5/' requirements.txt && \
    grep -v -E '^(amqp-worker|axial-positional-embedding|cloudpickle|lockfile|p-tqdm|pathos|pika|pox|ppft|product-key-memory|progressbar2|python-daemon|submitit|mkl-service|thop|flask)' requirements.txt > requirements_filtered.txt && \
    pip install --no-cache-dir -r requirements_filtered.txt && \
    pip install --no-cache-dir thop && \
    rm requirements_filtered.txt

# Install Flask with compatible dependencies
RUN pip install --no-cache-dir flask==2.0.0 werkzeug==2.0.0 jinja2==3.0.0 markupsafe==2.0.0

# Copy application code
COPY . .

# Make scripts executable
RUN chmod +x /home/ubuntu/deploy-projects/47bb5f3ab9460c0e249214c4/entrypoint.sh /home/ubuntu/deploy-projects/47bb5f3ab9460c0e249214c4/health_server.py

# Default command: run entrypoint
CMD ["./entrypoint.sh"]