FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV OMP_NUM_THREADS=8
ENV ARROW_DEFAULT_MEMORY_POOL=system

WORKDIR /home/ubuntu/deploy-projects/66995efbaed073388e2eae8d

# Install system dependencies including redis, curl and netcat for healthcheck
RUN apt-get update && apt-get install -y curl unzip redis-server netcat-openbsd procps && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY setup.py .
# Pin sqlglot to version that has dataframe module (20.x had it, 28.x removed it)
RUN pip install --no-cache-dir "sqlglot>=11.4.2,<21" .

# Copy application code
COPY pyquokka/ ./pyquokka/

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o /tmp/awscliv2.zip && \
    unzip -q /tmp/awscliv2.zip -d /tmp && \
    /tmp/aws/install && \
    rm -rf /tmp/awscliv2.zip /tmp/aws

# Expose internal port for Flight server
EXPOSE 5005

# Start Flight server and Redis in background
CMD bash -c "redis-server pyquokka/redis.conf --port 6800 --protected-mode no & \
    python -c \"from pyquokka.flight import FlightServer; s = FlightServer('0.0.0.0', location='grpc+tcp://0.0.0.0:5005'); s.serve()\""