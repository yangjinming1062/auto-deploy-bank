FROM python:3.10-slim

# Install curl for healthcheck and build dependencies
# freetype-dev, pkg-config, and make needed for matplotlib
RUN apt-get update && apt-get install -y curl libyaml-dev libfreetype-dev pkg-config make && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    CUDA_VISIBLE_DEVICES=0 \
    MASTER_ADDR=127.0.0.1 \
    MASTER_PORT=15000 \
    NCCL_SOCKET_FAMILY=AF_INET \
    GLOO_SOCKET_FAMILY=AF_INET \
    KMP_DUPLICATE_LIB_OK=TRUE

WORKDIR /home/ubuntu/deploy-projects/4ec1597e9a5c54f30b4edbec

# Install build dependencies first
RUN pip install --no-cache-dir --upgrade pip wheel

# Copy requirements and install dependencies
COPY requirements.txt .
# Update package versions for Python 3.10 compatibility
RUN sed -i 's/pyyaml==5.4.1/pyyaml>=6.0/' requirements.txt && \
    sed -i 's/matplotlib==3.4.2/matplotlib>=3.7.0/' requirements.txt && \
    sed -i 's/tensorboard==2.12.0/tensorboard>=2.13.0/' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 11234

# Start the Gradio application
CMD ["python", "app.py"]