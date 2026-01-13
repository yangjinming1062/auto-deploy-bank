# Use an official PyTorch base image with CUDA support
FROM pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    ca-certificates \
    git \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install flask==3.0.0

# Copy the rest of the application code (including scripts like downloads.sh)
COPY . .

# Set environment variables for CUDA
ENV CUDA_VISIBLE_DEVICES=0

# Make the downloads.sh script executable
RUN chmod +x ./downloads.sh

# Download required datasets using the downloads.sh script
RUN ./downloads.sh

# Set up the .env file
RUN cp ./.env.template ./.env

# Expose the API server port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Command to run the API server by default (can be overridden for direct experiment runs)
CMD ["python", "./api_server.py"]
