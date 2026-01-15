FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV QT_QPA_PLATFORM=offscreen

# Install system dependencies for FastAPI server
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    openssl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/945b57a8a33541d3b577294e

# Copy requirements first for better caching
COPY requirements_minimal.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_minimal.txt

# Copy application code
COPY . .

# Create a wrapper script to start the FastAPI server
RUN echo '#!/bin/bash\n\
python server_main.py\n' > /home/ubuntu/deploy-projects/945b57a8a33541d3b577294e/start.sh && chmod +x /home/ubuntu/deploy-projects/945b57a8a33541d3b577294e/start.sh

CMD ["/home/ubuntu/deploy-projects/945b57a8a33541d3b577294e/start.sh"]