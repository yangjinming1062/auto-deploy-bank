FROM python:3.11-slim

# Install system dependencies for OpenCV and other packages
RUN apt-get update && apt-get install -y \
    curl \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV IU_HOME=/root/.cache/dghs-imgutils
ENV HF_TOKEN=${HF_TOKEN:-}

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/512152ef90c70f1677e8e718

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies (exclude pilmoji temporarily due to build issue with 2.0.5)
RUN sed '/pilmoji/d' requirements.txt > /tmp/requirements-fixed.txt && \
    pip install --no-cache-dir -r /tmp/requirements-fixed.txt

# Install pilmoji from PyPI wheel (avoid broken 2.0.5 sdist)
RUN pip install --no-cache-dir "pilmoji>=1.3.0,!=2.0.5"

# Install gradio for demo
RUN pip install --no-cache-dir "gradio>=4.44.0"

# Copy application code
COPY . .

# Expose default Gradio port
EXPOSE 7860

# Run the demo service
CMD ["python", "demo.py", "--host", "0.0.0.0", "--port", "7860"]