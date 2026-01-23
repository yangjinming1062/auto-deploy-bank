# Ultralytics YOLO - RGBT Object Detection
FROM python:3.10-slim

# Install curl, procps, and OpenCV dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl procps libgl1 libglib2.0-0 libsm6 libxcb1 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_BREAK_SYSTEM_PACKAGES=1 \
    MKL_THREADING_LAYER=GNU \
    OMP_NUM_THREADS=1 \
    RANK=-1 \
    LOCAL_RANK=-1 \
    YOLO_AUTOINSTALL=true \
    YOLO_VERBOSE=true \
    YOLO_TQDM_RICH=false \
    YOLO_OFFLINE=false \
    CUDA_VISIBLE_DEVICES=-1

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/1965570298e101bafe84e0d7

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Healthcheck - verify Python and YOLO are working
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import ultralytics; print('YOLO Ultralytics container is running')" || exit 1

# Default command - start the web API server
CMD ["python", "web_api.py"]