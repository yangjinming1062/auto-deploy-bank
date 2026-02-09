FROM python:3.10-slim

# Install curl for healthcheck and protobuf for tokenizers
RUN apt-get update && apt-get install -y curl protobuf-compiler libprotobuf-dev && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/03a8525cb7184c50f90bfb31

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GRADIO_TEMP_DIR=.gradio_cache
ENV TOKENIZERS_PARALLELISM=false

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p .gradio_cache outputs

# Expose the internal port
EXPOSE 7860

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the application
CMD ["python", "scripts/demo_gradio.py"]