FROM python:3.6-slim

ENV PYTHONUNBUFFERED=1
ENV TF_CPP_MIN_LOG_LEVEL=2
ENV CUDA_VISIBLE_DEVICES=0

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/c26352f49a30058c729322d5

# Copy and install Python dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Flask for web service wrapper
RUN pip install --no-cache-dir flask

# Copy application code
COPY . .

# Pre-download data to avoid runtime network issues
RUN mkdir -p Data_manager_split_datasets/Movielens1M && \
    if [ ! -f Data_manager_split_datasets/Movielens1M/ml-1m.zip ]; then \
        curl -L -o Data_manager_split_datasets/Movielens1M/ml-1m.zip \
        http://files.grouplens.org/datasets/movielens/ml-1m.zip; \
    fi

# Run Flask web service
CMD ["python", "run_service.py"]