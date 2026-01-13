FROM python:3.11-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Configure apt to use multiple mirrors and retry
RUN echo 'Acquire::Retries "3";' > /etc/apt/apt.conf.d/80-retries && \
    echo 'Acquire::http::Timeout "30";' >> /etc/apt/apt.conf.d/80-retries && \
    echo 'Acquire::ftp::Timeout "30";' >> /etc/apt/apt.conf.d/80-retries

# Update package list with retries and install system dependencies
RUN apt-get update --fix-missing && \
    apt-get install -y --fix-missing --no-install-recommends \
    libreoffice \
    default-jre \
    poppler-utils \
    git \
    curl \
    ca-certificates \
    libgl1 \
    libglib2.0-0 \
    fonts-dejavu \
    fonts-dejavu-core \
    fonts-dejavu-extra \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set working directory
WORKDIR /app

# Copy minimal requirements for better caching
COPY requirements-minimal.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy patch script
COPY patch_gradio_client.py /tmp/

# Run patch script
RUN python3 /tmp/patch_gradio_client.py

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /data /runs /tmp

# Create startup script
RUN echo '#!/bin/bash\necho "OPENAI_API_KEY=$OPENAI_API_KEY" > /app/.env\necho "GOOGLE_SEARCH_API_KEY=$GOOGLE_SEARCH_API_KEY" >> /app/.env\necho "GOOGLE_SEARCH_ENGINE_ID=$GOOGLE_SEARCH_ENGINE_ID" >> /app/.env\ncd /app\nexport PYTHONPATH=/app:$PYTHONPATH\nexec "$@"' > /entrypoint.sh && chmod +x /entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command - launch Gradio web service
CMD ["python", "demo/app.py"]
