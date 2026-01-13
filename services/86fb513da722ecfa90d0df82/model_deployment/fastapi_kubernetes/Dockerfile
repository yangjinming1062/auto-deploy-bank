FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install curl and build dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    gcc \
    g++ \
    gfortran \
    libblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY ./app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app .

EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:80/ || exit 1

# Start command - using main:app since files are copied to /app root
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
