FROM python:3.9-slim

WORKDIR /app

# Install curl for healthcheck and build dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DRAGGAN_HOME=/app/checkpoints

# Copy requirements first for better caching
COPY requirements.txt .

# Install PyTorch CPU version first, then other dependencies
RUN pip install --no-cache-dir \
    torch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir ninja \
    && pip install --no-cache-dir "numpy<2"

# Copy application code
COPY . .

# Expose the port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Start the application
CMD ["python", "gradio_app.py", "--device", "cpu", "--ip", "0.0.0.0", "-p", "7860"]
