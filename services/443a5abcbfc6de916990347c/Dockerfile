FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck and Flask for web server
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir flask

WORKDIR /home/ubuntu/deploy-projects/443a5abcbfc6de916990347c

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Default command - run Flask web server
CMD ["python", "web_server.py"]