FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/home/ubuntu/deploy-projects/846754d5b4bf117f2a445f99/src:$PYTHONPATH

WORKDIR /home/ubuntu/deploy-projects/846754d5b4bf117f2a445f99

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install tanuki package in editable mode
RUN pip install --no-cache-dir -e .

# Expose the internal port
EXPOSE 8000

# Command to run the FastAPI application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]