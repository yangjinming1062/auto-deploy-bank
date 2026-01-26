FROM python:3.10-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/20c352138f89642948c75843

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV WANDB_DISABLE_CODE=true
ENV DEBIAN_FRONTEND=noninteractive

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add Flask to requirements (not in requirements.txt)
RUN pip install --no-cache-dir flask

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]