# MGANPrior - Image Processing Using Multi-Code GAN Prior

FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TF_CPP_MIN_LOG_LEVEL=2
ENV CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0}
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libgl1 \
    libglib2.0-0 \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    liblcms2-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory first
WORKDIR /home/ubuntu/deploy-projects/5e835950885bea5d1bde90ea

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "5000"]