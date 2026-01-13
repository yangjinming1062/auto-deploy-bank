# Use Python 3.10 slim image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files from prepared directory
COPY rag_app/requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    pip install --no-cache-dir langchain-community langchain-core langchain-text-splitters langchain sentence-transformers

# Copy application code
COPY rag_app/ /app/

# Create necessary directories
RUN mkdir -p /app/chroma_db /app/data

# Change to app directory
WORKDIR /app

# Expose internal port
EXPOSE 5002

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5002/ || exit 1

# Start the Flask application
CMD ["python", "-u", "app.py"]