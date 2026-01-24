FROM python:3.10-slim

# Install curl for healthcheck and OpenCV dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libegl1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TOKENIZERS_PARALLELISM=false
ENV DATA_PATH=./data
ENV OUTPUT_DIR=./output

WORKDIR /home/ubuntu/deploy-projects/a5645506a261b37bbece66e1

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create output directory
RUN mkdir -p output

# Copy and set up startup script
COPY run_musc.sh /home/ubuntu/deploy-projects/a5645506a261b37bbece66e1/run_musc.sh
RUN chmod +x /home/ubuntu/deploy-projects/a5645506a261b37bbece66e1/run_musc.sh

# Default command - runs MuSc via startup script
CMD ["/home/ubuntu/deploy-projects/a5645506a261b37bbece66e1/run_musc.sh"]