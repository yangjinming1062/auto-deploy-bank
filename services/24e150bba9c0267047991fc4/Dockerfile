FROM python:3.11-slim

WORKDIR /app

# Install curl for potential debugging
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set Python to output unbuffered
ENV PYTHONUNBUFFERED=1

# Run the web server by default
# Use: docker compose run dynasaur python dynasaur.py [args] to run CLI mode
CMD ["python", "web.py"]