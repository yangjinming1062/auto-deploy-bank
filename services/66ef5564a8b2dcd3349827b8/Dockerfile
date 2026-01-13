FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies including curl for healthcheck and build tools
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    cmake \
    libboost-all-dev \
    libx11-dev \
    libgtk-3-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Copy requirements and install Python dependencies
# Install root requirements first (ML/AI core dependencies)
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Then install API-specific requirements
COPY api/requirements.txt ./api/requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt

# Copy application files
COPY api/ ./api/
COPY Web/ ./Web/
COPY main.py .
COPY params.py .

# Ensure the Rust binary is executable
RUN chmod +x api/subtitle_search_api

# Expose port 8000
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["python", "api/index.py"]