FROM python:3.11-slim

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/81715960920a17f244f299e5

# Copy requirements first for better caching
COPY requirements-minimal.txt requirements.txt

# Install Python dependencies with pre-compiled wheels preference
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/home/ubuntu/deploy-projects/81715960920a17f244f299e5

# Expose Flask port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/sms || exit 1

# Run Flask server
CMD ["python", "stock_data/stock_twilio_server.py"]