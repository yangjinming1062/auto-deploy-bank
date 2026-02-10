FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/home/ubuntu/deploy-projects/6022569a8a483a469b59535e/python

WORKDIR /home/ubuntu/deploy-projects/6022569a8a483a469b59535e/python/samples/demos/process_with_dapr

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY python/samples/demos/process_with_dapr/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the semantic-kernel Python package
COPY python/semantic_kernel/ ./semantic_kernel/
COPY python/pyproject.toml .
COPY python/README.md .
COPY python/LICENSE .

# Install semantic-kernel in editable mode
RUN pip install --no-cache-dir -e . -f /home/ubuntu/deploy-projects/6022569a8a483a469b59535e

# Copy the demo app files
COPY python/samples/demos/process_with_dapr/fastapi_app.py ./fastapi_app.py
COPY python/samples/demos/process_with_dapr/flask_app.py ./flask_app.py
COPY python/samples/demos/process_with_dapr/process ./process

# Expose the internal port
EXPOSE 5001

# Run the FastAPI application with uvicorn
CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "5001"]