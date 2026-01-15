FROM python:3.7-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/c962562e87fd384f1f3b02df

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 5000

# Use gunicorn as the production server
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "2"]