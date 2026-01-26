# MindSpore Training Web Service Dockerfile
FROM python:3.10-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/326954989377af217712135e

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=40985
ENV DEVICE_ID=0
ENV DEVICE_NUM=1
ENV RANK_ID=0
ENV RANK_SIZE=1
ENV RANK_TABLE_FILE=
ENV MINDSPORE_HCCL_CONFIG_PATH=
ENV MS_ROLE=MS_WORKER
ENV GLOG_v=0
ENV GLOG_log_dir=
ENV ASCEND_GLOBAL_LOG_LEVEL=0

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the Flask web server in foreground
CMD ["python", "webapp.py"]