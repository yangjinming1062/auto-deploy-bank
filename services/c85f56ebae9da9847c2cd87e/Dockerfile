FROM python:3.10-slim

# Install system dependencies for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    TOKENIZERS_PARALLELISM=false \
    KMP_DUPLICATE_LIB_OK=True \
    HF_HOME=/tmp/huggingface \
    TRANSFORMERS_CACHE=/tmp/transformers

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/c85f56ebae9da9847c2cd87e

# Copy requirements first for better caching
COPY pip_requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r pip_requirements.txt

# Copy application code
COPY . .

# Create directories for models and caches
RUN mkdir -p /tmp/huggingface /tmp/transformers /tmp/data

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application with uvicorn for web server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]