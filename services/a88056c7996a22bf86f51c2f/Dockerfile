FROM python:3.11-slim

WORKDIR /home/ubuntu/deploy-projects/a88056c7996a22bf86f51c2f

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=41221

# Expose the web server port
EXPOSE 41221

# Default command - run the Flask web server
CMD ["python", "webserver.py"]