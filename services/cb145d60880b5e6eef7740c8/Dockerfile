FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/cb145d60880b5e6eef7740c8

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install aiohttp from PyPI (pre-built wheels)
RUN pip install --no-cache-dir aiohttp

# Copy application code
COPY app.py .

EXPOSE 8080

CMD ["python", "app.py"]