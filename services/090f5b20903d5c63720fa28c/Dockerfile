# Dockerfile for Libra ML Library - Streamlit Dashboard
FROM python:3.10-slim

# Install system dependencies required for ML libraries
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    make \
    cmake \
    pkg-config \
    libgl1-mesa-dri \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    tk \
    tcl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    TF_CPP_MIN_LOG_LEVEL=3

WORKDIR /home/ubuntu/deploy-projects/090f5b20903d5c63720fa28c

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies with optimizations
# Use --only-binary for packages with available wheels
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir \
        tensorflow-cpu==2.12.0 \
        keras==2.12.0 \
        keras-preprocessing \
        numpy \
        pandas \
        scikit-learn==1.1.3 \
        matplotlib \
        seaborn \
        xgboost \
        opencv-python-headless \
        nltk \
        spacy \
        altair \
        streamlit \
        colorama \
        transformers==4.20.1 \
        tabulate \
        textblob \
        keras-tuner \
        jellyfish \
        autocorrect \
        pillow \
        prince \
        download

# Copy application code
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit dashboard
CMD ["streamlit", "run", "libra/dashboard/LibEDA.py", "--server.port=8501", "--server.address=0.0.0.0"]