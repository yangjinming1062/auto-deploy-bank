FROM python:3.11-slim

# Install system dependencies including curl for healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        && rm -rf /var/lib/apt/lists/*

ENV GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV PYTHONUNBUFFERED=1

EXPOSE 7860

WORKDIR /app

# Create and activate virtual environment
RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies
COPY requirements.txt setup.py README.md /app/
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code and necessary directories
COPY docext /app/docext
COPY assets /app/assets
COPY configs /app/configs
COPY MANIFEST.in /app/MANIFEST.in

# Install application
RUN pip install --no-cache-dir -e .

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:7860/ || exit 1

# Set working directory and entrypoint
WORKDIR /app/
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser
USER appuser
ENTRYPOINT ["/app/.venv/bin/python", "-m", "docext.app.app", "--model_name", "openai/gpt-4o", "--no-share", "--server_port", "7860"]