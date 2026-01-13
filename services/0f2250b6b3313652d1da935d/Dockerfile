# Zero to NLP - Chinese NLP Training Framework
FROM python:3.10-slim

# Set working directory
WORKDIR /home/ubuntu/deploy-projects

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install additional ML dependencies commonly used in the framework
RUN pip install --no-cache-dir \
    torch \
    torchvision \
    torchaudio \
    deepspeed \
    accelerate \
    peft \
    bitsandbytes \
    xformers \
    tensorboard \
    jupyter \
    jupyterlab \
    ipywidgets \
    matplotlib \
    seaborn \
    scikit-learn \
    tqdm \
    wandb \
    datasets \
    evaluate \
    sentencepiece

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p output_dir cache_data model_result

# Expose port for Gradio app
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the main application
CMD ["python", "main_app.py"]