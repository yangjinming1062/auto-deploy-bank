FROM python:3.6-slim

ENV PYTHONUNBUFFERED=1 \
    TF_CPP_MIN_LOG_LEVEL=2 \
    CUDA_VISIBLE_DEVICES=0 \
    FLASK_HOST=0.0.0.0 \
    FLASK_PORT=5000

# Install curl for healthcheck and system dependencies for MIDI processing
RUN apt-get update && apt-get install -y curl libasound2-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/ed6150e19f5fb6553e560882

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]