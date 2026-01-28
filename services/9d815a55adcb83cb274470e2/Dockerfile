FROM python:3.11-slim

WORKDIR /home/ubuntu/deploy-projects/9d815a55adcb83cb274470e2

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set Python environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/home/ubuntu/deploy-projects/9d815a55adcb83cb274470e2/src:$PYTHONPATH

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add FastAPI and uvicorn to requirements during install
RUN pip install --no-cache-dir fastapi uvicorn

# Copy application code
COPY . .

# Expose the internal port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]