FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set Python environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/ee2a533d8b92db80eb34ff12

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
# Note: onnxruntime-directml is Windows-only. For Linux, we use onnxruntime (CPU) instead
# langchain 0.2.x has the old chain module structure needed by this script
RUN sed -i 's/onnxruntime-directml>=1.15.0/onnxruntime>=1.15.0/g' requirements.txt && \
    sed -i 's/^langchain$/langchain==0.2.17/g' requirements.txt && \
    sed -i 's/^optimum$/optimum[onnxruntime]>=1.0.0/g' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir langchain-community==0.2.17 langchain-text-splitters==0.2.4 Pillow

# Copy application code
COPY . .

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Run the entrypoint script which patches for Linux compatibility
ENTRYPOINT ["./entrypoint.sh"]