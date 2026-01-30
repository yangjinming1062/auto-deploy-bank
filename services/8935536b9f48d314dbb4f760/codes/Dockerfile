FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    CUDA_GRAPHS=0 \
    PAYLOAD_LIMIT=8000000 \
    HF_TOKEN=${HF_TOKEN}

WORKDIR /home/ubuntu/deploy-projects/8935536b9f48d314dbb4f760

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy dependency files first for better layer caching
COPY codes/pyproject.toml codes/README.md .

# Install project dependencies
RUN pip install --no-cache-dir \
    matplotlib>=3.10.3 \
    pillow>=11.2.1 \
    pyautogui>=0.9.54 \
    && pip install --no-cache-dir -e .

# Copy application code
COPY codes/ui_tars/ ./codes/ui_tars/
COPY codes/tests/ ./codes/tests/

# Keep container running for healthcheck
CMD ["python", "-c", "import time; time.sleep(float('inf'))"]