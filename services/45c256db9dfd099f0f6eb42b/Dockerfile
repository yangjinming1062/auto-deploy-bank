FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies and curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    torch>=2.0.0 \
    dgl>=1.0 \
    transformers>=4.3.0 \
    ogb==1.3.6 \
    torchdata>=0.9.0 \
    pyarrow>=12.0.0 \
    h5py>=3.8.0 \
    pydantic>=2.0.0 \
    scikit-learn>=1.2.0 \
    boto3>=1.26.0 \
    numpy>=1.23.0 \
    psutil>=5.9.0 \
    pyyaml>=6.0 \
    flask>=2.0.0 \
    gunicorn>=21.0.0

# Copy GraphStorm source
RUN mkdir -p /graphstorm/python
COPY python/graphstorm /graphstorm/python/graphstorm

# Set up Python path and working directory
ENV PYTHONPATH="/graphstorm/python:${PYTHONPATH}"
WORKDIR /graphstorm

# Copy entrypoint script
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy webapp
COPY docker/webapp.py /webapp.py

EXPOSE 40219

# Healthcheck using SSH port check (or process check)
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD pgrep -x sshd > /dev/null || exit 1

ENTRYPOINT ["/entrypoint.sh"]