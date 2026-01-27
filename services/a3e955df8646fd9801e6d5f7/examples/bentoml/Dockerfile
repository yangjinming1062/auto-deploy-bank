# Runtime stage for BentoML Whisper service
FROM python:3.11-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV XDG_DATA_HOME=/home/bentoml/.local/share
ENV BENTOML_HOME=/home/bentoml/.local/share/bentoml
ENV HF_HUB_DISABLE_XDG=1

# Create data directories for models
RUN mkdir -p ${XDG_DATA_HOME}/whispercpp

# Install Python dependencies
COPY examples/bentoml/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install whispercpp from pre-built wheel
RUN pip install --no-cache-dir whispercpp

# Copy service files
COPY examples/bentoml/service.py .

# Expose internal port (BentoML default)
EXPOSE 3000

# Healthcheck - check if service is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

# Run BentoML service
CMD ["bentoml", "serve", "service:WhisperService", "--host", "0.0.0.0", "--port", "3000"]