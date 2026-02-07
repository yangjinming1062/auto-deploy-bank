FROM python:3.10-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/80695c8eb14090459936a888

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies - install torch CPU first, then rest from requirements
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install --default-timeout=600 -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /home/ubuntu/deploy-projects/80695c8eb14090459936a888/data/chroma_data \
    /home/ubuntu/deploy-projects/80695c8eb14090459936a888/data/nebula_data \
    /home/ubuntu/deploy-projects/80695c8eb14090459936a888/logs \
    /home/ubuntu/deploy-projects/80695c8eb14090459936a888/jupyter_work

# Expose the main API port
EXPOSE 7861

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7861/ || exit 1

# Start the FastAPI server using Python module execution
CMD ["python", "-m", "uvicorn", "examples.api:app", "--host", "0.0.0.0", "--port", "7861"]