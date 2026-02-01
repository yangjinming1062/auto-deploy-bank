FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/fbed593fac147080c5ccb96f

# Copy requirements first for better caching
COPY requirements.txt .
COPY server.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY configs/ ./configs/
COPY m3_agent/ ./m3_agent/
COPY mmagent/ ./mmagent/
COPY data/ ./data/

# Expose the internal port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Start the Flask server
CMD ["python", "server.py"]