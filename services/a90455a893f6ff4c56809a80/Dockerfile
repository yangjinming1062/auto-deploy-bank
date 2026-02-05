FROM python:3.11-slim

# Install system dependencies for audio and compilation
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    cmake \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LANG=EN
ENV DEBUG=true
ENV WHISP_PATH=models/whisper-large-v3
ENV MODEL_PATH=models/yi-34b-chat.Q8_0.gguf
ENV CHUNK=1024
ENV CHANNELS=1
ENV RATE=44100
ENV SILENCE_THRESHOLD=500
ENV MIC_IDX=0

# Create working directory
WORKDIR /home/ubuntu/deploy-projects/a90455a893f6ff4c56809a80

# Copy requirements first for better cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (excluding local whisper which is macOS-only)
COPY main.py .
COPY webserver.py .
COPY static/ static/
COPY prompts/ prompts/
COPY tools/ tools/
# Remove local whisper directory - we'll use pip package openai-whisper instead

# Create directories for models and recordings
RUN mkdir -p models recordings

# Run the web server
CMD ["python", "webserver.py"]