FROM python:3.10-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV XDG_CACHE_HOME=/root/.cache

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/73ab573abc7400fd24b12576

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 5011

# Start the application
CMD ["python", "app.py"]