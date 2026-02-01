FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl zip && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
# Note: flash-attn requires CUDA/GPU, so we skip it for CPU-only environments
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir arxiv wandb rich lxml bs4 flask && \
    pip install --no-cache-dir torch transformers numpy

# Create data directories and placeholder files
RUN mkdir -p data/paper_database checkpoints && \
    echo '{}' > data/paper_database/id2paper.json && \
    touch data/paper_database/cs_paper_2nd.zip

# Copy application code
COPY . .

# Default command
CMD ["python", "run_paper_agent.py"]