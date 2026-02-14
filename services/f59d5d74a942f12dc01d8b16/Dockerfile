FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Install curl, git and build essentials for compiling Python packages
RUN apt-get update && apt-get install -y curl git build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better layer caching
COPY hugginggpt/server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade flask "werkzeug>=2.2.2" && \
    pip install --no-cache-dir huggingface_hub==0.19.4

# Copy application code
COPY hugginggpt/server/ .

# Create required directories
RUN mkdir -p logs public/images public/audios public/videos data demos

EXPOSE 8004

CMD ["python", "awesome_chat.py", "--config", "configs/config.default.yaml", "--mode", "server"]