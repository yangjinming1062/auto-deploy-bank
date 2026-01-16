FROM python:3.10-slim

# Install system dependencies and curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    pkg-config \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=0
ENV NVIDIA_VISIBLE_DEVICES=0

WORKDIR /home/ubuntu/deploy-projects/8d065569bcbc0d1a35727433

# Copy requirements and install dependencies
COPY requirements.txt .

# Upgrade pip first
RUN pip install --no-cache-dir --upgrade pip

# Install torch and torchaudio CPU version first (required by masr)
RUN pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install packages that have pre-built wheels (pure Python or binary wheels)
RUN pip install --no-cache-dir --only-binary=:all: \
    numpy \
    scipy \
    tqdm \
    cython \
    pyyaml \
    requests \
    termcolor \
    websockets \
    zhconv \
    ijson \
    flask \
    flask-cors \
    ffmpeg-python \
    cn2an

# Install python-Levenshtein with a compatible version
RUN pip install --no-cache-dir "python-Levenshtein>=0.12.2,<0.21.0"

# Install remaining dependencies
RUN pip install --no-cache-dir \
    visualdl>=2.1.1 \
    SoundFile~=0.10 \
    resampy==0.2.2 \
    numba>=0.53.0 \
    webrtcvad~=2.0.10 \
    pydub~=0.25.1 \
    WeTextProcessing>=0.0.4 \
    audioread~=2.1.9

# Try installing librosa with deps
RUN pip install --no-cache-dir librosa~=0.9.2

# Copy application code
COPY . .

# Expose ports (Flask on 5000, WebSocket streaming on 5001)
EXPOSE 5000 5001

# Start the server
CMD ["python", "infer_server.py", "--configs=configs/config_zh.yml", "--host=0.0.0.0"]