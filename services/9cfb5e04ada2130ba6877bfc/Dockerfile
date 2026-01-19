FROM python:3.10-slim

WORKDIR /home/ubuntu/deploy-projects/9cfb5e04ada2130ba6877bfc

# Install system dependencies for healthcheck and basic operations
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set Python environment
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    LOGDIR=/home/ubuntu/deploy-projects/9cfb5e04ada2130ba6877bfc/data/logs \
    CONVERSATION_SAVE_DIR=/home/ubuntu/deploy-projects/9cfb5e04ada2130ba6877bfc/data/conversation_data

# Create necessary directories for logging and data
RUN mkdir -p /home/ubuntu/deploy-projects/9cfb5e04ada2130ba6877bfc/data/logs \
    /home/ubuntu/deploy-projects/9cfb5e04ada2130ba6877bfc/data/conversation_data \
    /home/ubuntu/deploy-projects/9cfb5e04ada2130ba6877bfc/data/images

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the Gradio port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Start command - controller URL uses Docker network hostname
CMD ["python", "server_demo.py", "--host", "0.0.0.0", "--port", "7860", "--controller-url", "http://controller:12001"]