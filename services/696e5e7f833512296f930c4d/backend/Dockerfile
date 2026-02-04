FROM --platform=linux/amd64 python:3.11-slim

# Required for opencv and healthcheck
RUN apt-get update -y && \
    apt-get install --no-install-recommends ffmpeg libsm6 libxext6 curl -y && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH=/virtualenvs/venv/bin:$PATH
RUN python3 -m venv /virtualenvs/venv/

# Copy requirements.txt
COPY backend/requirements.txt /tmp/requirements.txt
COPY backend/vectordb.requirements.txt /tmp/vectordb.requirements.txt

# Install Python packages
RUN python3 -m pip install -U pip setuptools wheel uv && \
    python3 -m uv pip install --no-cache-dir -r /tmp/requirements.txt --index-strategy unsafe-any-match && \
    playwright install --with-deps

# Install VectorDB packages
ARG ADD_VECTORDB=0
RUN if [ "${ADD_VECTORDB}" = "1" ]; then python3 -m uv pip install --no-cache-dir -r /tmp/vectordb.requirements.txt --index-strategy unsafe-any-match; fi

# Copy the project files
COPY . /app

# Set the working directory
WORKDIR /app

# Environment variables
ENV PYTHONUNBUFFERED=1

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health-check || exit 1

# Run the application
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "backend.server.app:app"]
