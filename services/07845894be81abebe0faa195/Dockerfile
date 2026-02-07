FROM python:3.12-slim

# Install curl and build dependencies for pandas compilation
RUN apt-get update && apt-get install -y curl gcc g++ build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/07845894be81abebe0faa195

# Copy requirements and install dependencies (excluding pandas-stubs for faster/simpler install)
COPY src/requirements.txt .
RUN grep -v "pandas-stubs" requirements.txt | xargs pip install --no-cache-dir

# Copy the entire source code
COPY src/ .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LOGURU_LEVEL=TRACE
ENV TOKENIZERS_PARALLELISM=false

# Expose the internal port (default HTTP server port)
EXPOSE 8080

# Run HTTP server for basic file serving
CMD ["python", "-m", "http.server", "8080"]