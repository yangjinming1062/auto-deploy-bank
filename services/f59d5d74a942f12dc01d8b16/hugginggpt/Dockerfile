FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better layer caching
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server/ .

# Create required directories
RUN mkdir -p logs public/images public/audios public/videos data demos

EXPOSE 8004

CMD ["python", "awesome_chat.py", "--config", "configs/config.default.yaml", "--mode", "server"]