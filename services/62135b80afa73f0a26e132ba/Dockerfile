FROM python:3.11-slim

WORKDIR /home/ubuntu/deploy-projects/62135b80afa73f0a26e132ba

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY kimina_prover_demo/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY kimina_prover_demo/ .

# Expose the port the app runs on
EXPOSE 8080

# Run the server with uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]