FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV DIFFUSEBOT_ROOT=/home/ubuntu/deploy-projects/f5975caa9d2e1128c11173fd

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential curl git libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 libjpeg62-turbo && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/f5975caa9d2e1128c11173fd

# Copy requirements first for better caching
COPY requirements.txt .

# Install ALL Python dependencies in a SINGLE RUN command to prevent timeout
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && pip install --no-cache-dir torch==1.13.1 torchvision && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create cache directory
RUN mkdir -p /home/ubuntu/deploy-projects/f5975caa9d2e1128c11173fd/cache /home/ubuntu/deploy-projects/f5975caa9d2e1128c11173fd/results

# Default command - run Flask app
CMD ["python", "app.py"]