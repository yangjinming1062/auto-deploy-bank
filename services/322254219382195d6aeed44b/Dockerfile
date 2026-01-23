FROM python:3.11-slim

WORKDIR /home/ubuntu/deploy-projects/322254219382195d6aeed44b

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set Python environment variable
ENV PYTHONUNBUFFERED=1

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install PyTorch (CPU only) for system requirements check
# The proxy server routes requests to vLLM servers, so only CPU is needed
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Copy application code
COPY . .

# Install the package in development mode
RUN pip install --no-cache-dir -e .

# Expose default proxy port
EXPOSE 8000

# Health check using the proxy health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the proxy server (default port 8000)
CMD ["vllm-cli", "proxy", "start", "--host", "0.0.0.0", "--port", "8000"]