FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install graphrag from PyPI (avoids build issues with monorepo structure)
RUN pip install --no-cache-dir "graphrag>=3.0.0" "uvicorn>=0.30.0" "fastapi>=0.110.0"

# Copy the server.py file for the API
COPY server.py .

# Copy the rest of the application
COPY . .

EXPOSE 8000

CMD ["python", "server.py"]