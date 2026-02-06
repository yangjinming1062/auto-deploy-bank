FROM python:3.9-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/bfb55e65838ad45299edeebb

# Set Python environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/home/ubuntu/deploy-projects/bfb55e65838ad45299edeebb
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make startup script executable
RUN chmod +x /home/ubuntu/deploy-projects/bfb55e65838ad45299edeebb/start.sh

# Expose tensorboard port (default 6006)
EXPOSE 6006

# Healthcheck - verify TensorBoard is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:6006 || exit 1

# Run startup script (TensorBoard or training)
CMD ["/home/ubuntu/deploy-projects/bfb55e65838ad45299edeebb/start.sh"]