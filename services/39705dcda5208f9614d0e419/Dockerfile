FROM python:3.12-slim

WORKDIR /app

# Install system dependencies and curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender1 \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Create result directory
RUN mkdir -p /app/result && chmod 1777 /app/result

# Create tmp directory with proper permissions
RUN rm -rf /tmp && mkdir /tmp && chmod 1777 /tmp

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose the web server port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run the web server using server/main.py
CMD ["python", "server/main.py", "--host", "0.0.0.0", "--port", "8000", "--start-instance"]