FROM python:3.7-slim

# Install system dependencies and curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/1cff50108f7225c7819467f6

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make web_server.py executable
RUN chmod +x web_server.py

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GIT_PYTHON_REFRESH=quiet
ENV KMP_DUPLICATE_LIB_OK=True
ENV CUDA_VISIBLE_DEVICES=0

# Expose port 40293 for web interface
EXPOSE 40293

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:40293/ || exit 1

# Start the application with web server wrapper
CMD ["python", "web_server.py"]