FROM python:3.8-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Flask for web server
RUN pip install --no-cache-dir flask==3.0.0

ENV PYTHONUNBUFFERED=1
ENV LOCAL_RANK=0
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV CUDA_VISIBLE_DEVICES=0

WORKDIR /home/ubuntu/deploy-projects/7d8151a6b7c58b5c72f3d323

# Copy requirements first for better caching
COPY pipelines/requirements.txt .
# Remove conflicting mkl packages that require older numpy versions
RUN grep -v -E "^(mkl-fft|mkl-random|mkl-service)" requirements.txt > requirements_clean.txt && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_clean.txt

# Install the pipelines package in editable mode
COPY pipelines/ .

# Create a simple healthcheck script
RUN echo "#!/bin/bash\npython -c \"import mmcv; import mmseg; print('OK')\" && exit 0 || exit 1" > /healthcheck.sh && chmod +x /healthcheck.sh

# Copy web server
COPY web_server.py /web_server.py

# Keep container running for healthcheck and start web server
CMD ["python", "/web_server.py"]