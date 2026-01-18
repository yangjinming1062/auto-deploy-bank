FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libjpeg62-turbo-dev \
    libpng-dev \
    libtiff-dev \
    libgtk-3-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV OMP_NUM_THREADS=1
ENV OPENBLAS_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV VECLIB_MAXIMUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1
ENV CUDA_VISIBLE_DEVICES=0

# Create app directory
WORKDIR /app

# Copy requirements from DiffIR-RealSR
COPY DiffIR-RealSR/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code from DiffIR-RealSR (main task)
COPY DiffIR-RealSR/ .

# Copy version.py which is ignored by gitignore
COPY DiffIR-RealSR/DiffIR/version.py DiffIR/version.py

# Set PYTHONPATH so DiffIR module imports work
ENV PYTHONPATH=/app

# Copy wrapper script
COPY DiffIR-RealSR/run_train.sh /app/run_train.sh
RUN chmod +x /app/run_train.sh

# Set working directory to /app for FastAPI service
WORKDIR /app

# Health check - verify python process is running
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD pgrep -f "python3" || exit 1

# Start the FastAPI web service
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8081"]