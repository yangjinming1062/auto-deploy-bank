FROM python:3.10-slim

# Install system dependencies for video processing and ML libraries
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV S3_VERIFY_SSL=1
ENV TF_CPP_MIN_LOG_LEVEL=2

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package in editable mode
RUN pip install --no-cache-dir -e .

EXPOSE 8001

CMD ["python", "web_server.py", "8001"]