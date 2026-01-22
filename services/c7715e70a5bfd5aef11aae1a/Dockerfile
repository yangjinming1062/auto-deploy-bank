FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxi6 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV HF_TOKEN=${HF_TOKEN:-}
ENV MODEL_NAME=Ruyi-Mini-7B
ENV MODEL_PATH=models/${MODEL_NAME}
ENV AUTO_DOWNLOAD=True
ENV CONFIG_PATH=config/default.yaml
ENV OUTPUT_DIR=outputs
ENV PORT=8080
ENV HOST=0.0.0.0
ENV KMP_DUPLICATE_LIB_OK=TRUE

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/c7715e70a5bfd5aef11aae1a

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for model and outputs
RUN mkdir -p ${MODEL_PATH} outputs

# Expose port
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application
CMD ["python", "app.py"]