FROM python:3.11-slim

# Install curl for healthcheck and protobuf for tokenizers
RUN apt-get update && apt-get install -y curl protobuf-compiler libprotobuf-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/03a8525cb7184c50f90bfb31

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TOKENIZERS_PARALLELISM=false
ENV GRADIO_TEMP_DIR=.gradio_cache
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir tiktoken protobuf

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p .gradio_cache outputs

# Expose the Gradio port
EXPOSE 7860

# Run the application
CMD ["python", "scripts/entrypoint.py"]