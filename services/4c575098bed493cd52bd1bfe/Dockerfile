FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/4c575098bed493cd52bd1bfe

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (for consistency, though this library doesn't run a web service)
EXPOSE 40252

# Run the application
CMD ["python", "run.py"]