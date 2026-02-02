FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Install curl, build essentials, PortAudio for pyaudio, and audio processing libraries
RUN apt-get update && apt-get install -y curl build-essential portaudio19-dev libsndfile1 ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/393f5a9897c2dfb272e3b629

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 5003

# Start command for FastAPI application
CMD ["python", "streaming_server.py", "--api_host", "0.0.0.0", "--api_port", "5003"]