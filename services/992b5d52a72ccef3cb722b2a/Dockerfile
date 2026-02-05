FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    FEAST_USAGE=True \
    FEAST_FORCE_LOCAL_UI=False \
    PYTHONPATH=/home/feast/sdk/python:$PYTHONPATH

# Install curl and build dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libc-dev \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/feast

# Copy requirements first for better caching
COPY sdk/python/feast/infra/feature_servers/multicloud/requirements.txt /home/feast/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /home/feast/requirements.txt

# Copy the Feast SDK source
COPY sdk/python/feast /home/feast/sdk/python/feast
COPY pyproject.toml setup.py /home/feast/
COPY patch_feature_server.py /usr/local/bin/patch_feature_server.py

# Create directories for feature store
RUN mkdir -p /home/feast/feature_repo/data && \
    chmod +x /usr/local/bin/patch_feature_server.py

# Expose the feature server port
EXPOSE 6565

# Healthcheck - check if feast feature server is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:6565/health || exit 1

# Start the Feast feature server
CMD ["sh", "-c", "python /usr/local/bin/patch_feature_server.py && feast serve --host 0.0.0.0 --port 6565"]