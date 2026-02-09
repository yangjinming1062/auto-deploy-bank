FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    VIDEO_FOLDER=/data/raw_videos \
    OUTPUT_FOLDER=/data/cropped_videos \
    WORKERS=4 \
    DEVICE_IDS=0 \
    YOUTUBE_DL_PATH=/usr/local/bin/youtube-dl

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    git \
    wget \
    cmake \
    libsm6 \
    libxext6 \
    libxrender1 \
    libfreetype6-dev \
    libpng-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install youtube-dl
RUN curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl \
    && chmod a+rx /usr/local/bin/youtube-dl

# Create directories for data volumes
RUN mkdir -p /data/raw_videos /data/cropped_videos /data/output

WORKDIR /home/ubuntu/deploy-projects/739b5abdb733d600939639a5

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip wheel setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Install face-alignment library (required for face detection)
RUN git clone https://github.com/1adrianb/face-alignment.git /tmp/face-alignment \
    && cd /tmp/face-alignment \
    && pip install --no-cache-dir -e . \
    && rm -rf /tmp/face-alignment

# Copy application code
COPY . .

# Create entrypoint script
COPY <<'EOF' /entrypoint.sh
#!/bin/bash
set -e

echo "Video Processing Service"
echo "========================="
echo "Available commands:"
echo "  - load_videos.py    : Download and process videos from YouTube"
echo "  - crop_vox.py       : Process VoxCeleb dataset (face detection + cropping)"
echo "  - crop_taichi.py    : Process TaiChi dataset (person detection + keypoints)"
echo "  - crop_nemo.py      : Process Nemo dataset (face detection + cropping)"
echo ""
echo "Environment variables:"
echo "  VIDEO_FOLDER   - Directory for raw videos (default: /data/raw_videos)"
echo "  OUTPUT_FOLDER  - Directory for processed output (default: /data/cropped_videos)"
echo "  WORKERS        - Number of parallel workers (default: 4)"
echo "  DEVICE_IDS     - GPU device IDs (default: 0)"
echo ""
echo "Example usage:"
echo "  docker compose run --rm processor python crop_vox.py --help"
echo "  docker compose run --rm processor python crop_vox.py --workers 4 --device_ids 0 --format .mp4"
echo ""

# Run the command passed to the container
exec "$@"
EOF
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Default command runs the Flask web server
CMD ["python", "webserver.py"]