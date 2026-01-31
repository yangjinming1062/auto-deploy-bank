FROM python:3.12-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/4e455498a11617da5f23495f

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy source files first for better caching
COPY pyproject.toml README.md ./
COPY trae_agent/ ./trae_agent/
COPY server/ ./server/

# Install the package with Docker support dependencies
RUN pip install --no-cache-dir -e . docker pexpect

# Default command - run the HTTP server
CMD ["python", "server/server.py"]