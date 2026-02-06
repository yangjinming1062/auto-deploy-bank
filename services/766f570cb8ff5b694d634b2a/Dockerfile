FROM python:3.7-slim

# Install curl and build tools for compiling packages
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TF_CPP_MIN_LOG_LEVEL=3
ENV PYTHONHASHSEED=0
ENV LOG_LEVEL=INFO

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/766f570cb8ff5b694d634b2a

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY health_server.py .

# Expose port
EXPOSE 8080

# Run the health server
CMD ["python", "health_server.py"]