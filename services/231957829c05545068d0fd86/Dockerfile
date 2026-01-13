FROM python:3.10-slim

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/231957829c05545068d0fd86

# Set environment variables to force CPU mode for bitsandbytes
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=.
ENV TOKENIZERS_PARALLELISM=false
ENV FORCE_CPU=1
ENV CUDA_VISIBLE_DEVICES=""
ENV BNB_DISABLE_TRITON=1

# Copy requirements and install Python dependencies
COPY requirements.txt .

# Install triton first (try to get CUDA version, but it's okay if it fails)
RUN pip install --no-cache-dir triton || echo "Triton installation failed, continuing with CPU-only mode"

# Install bitsandbytes with CPU-only mode (triton disabled)
RUN pip install --no-cache-dir bitsandbytes==0.38.1

# Install remaining Python dependencies
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy application code
COPY . .

# Create dummy corpus file with proper format for ToolRetriever
RUN printf "docid\tdocument_content\n" > dummy_corpus.tsv && printf "1\t{\"category_name\": \"Artificial_Intelligence_Machine_Learning\", \"tool_name\": \"test_tool\", \"api_name\": \"test_api\", \"api_description\": \"Test API for dummy data\", \"required_parameters\": {}, \"optional_parameters\": {}, \"template_response\": {}}\n" >> dummy_corpus.tsv && chmod +x start_server.sh

# Expose internal port
EXPOSE 5000

# Start the server (arguments will be provided via docker-compose)
CMD ["python", "toolbench/inference/toolbench_server.py"]