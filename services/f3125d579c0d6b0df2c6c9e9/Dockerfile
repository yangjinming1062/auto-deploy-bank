FROM python:3.10-slim

# Install system dependencies for ML libraries and curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/f3125d579c0d6b0df2c6c9e9

# Install CPU-only PyTorch and TensorFlow from official sources
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir tensorflow-cpu

# Copy requirements.txt and install remaining dependencies
# Remove pytorch/tensorflow (already installed) and inplace-abn (requires CUDA)
COPY requirements.txt .
RUN sed -i '/^pytorch/d' requirements.txt && \
    sed -i '/^tensorflow/d' requirements.txt && \
    sed -i '/^inplace-abn/d' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Install fastapi and uvicorn for web service
RUN pip install --no-cache-dir fastapi uvicorn

# Copy application code
COPY . .

# Expose the service port
EXPOSE 8000

# Health check using curl
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the FastAPI service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]