# Use Python slim base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    git \
    tor \
    tor-geoipdb \
    netcat-traditional \
    curl \
    build-essential \
    python3-dev \
    libffi-dev \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configure Tor - Simplified configuration
RUN echo "SocksPort 9050" >> /etc/tor/torrc && \
    echo "ControlPort 9051" >> /etc/tor/torrc && \
    echo "CookieAuthentication 1" >> /etc/tor/torrc && \
    echo "DataDirectory /var/lib/tor" >> /etc/tor/torrc

# Set correct permissions for Tor
RUN chown -R debian-tor:debian-tor /var/lib/tor && \
    chmod 700 /var/lib/tor

# Copy requirements first for better caching
COPY requirements.txt .

# Create and activate a virtual environment
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Upgrade pip and install dependencies with optimizations
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --prefer-binary --force-reinstall -r requirements.txt && \
    pip install --no-cache-dir PySocks>=1.7.1 requests[socks]>=2.28.1

# Install playwright and browser
RUN pip install --no-cache-dir playwright requests && \
    playwright install chromium && \
    playwright install-deps

# Copy application code
COPY . .

# Create run script with proper Tor startup
RUN echo '#!/bin/bash\n\
\n\
# Activate virtual environment\n\
source /app/venv/bin/activate\n\
\n\
# Start Tor service\n\
echo "Starting Tor service..."\n\
service tor start\n\
\n\
# Wait for Tor to be ready\n\
echo "Waiting for Tor to start..."\n\
for i in {1..30}; do\n\
    if ps aux | grep -v grep | grep -q /usr/bin/tor; then\n\
        echo "Tor process is running"\n\
        if nc -z localhost 9050; then\n\
            echo "Tor SOCKS port is listening"\n\
            break\n\
        fi\n\
    fi\n\
    if [ $i -eq 30 ]; then\n\
        echo "Warning: Tor might not be ready, but continuing..."\n\
    fi\n\
    sleep 1\n\
done\n\
\n\
# Verify Tor status\n\
echo "Checking Tor service status:"\n\
service tor status\n\
\n\
# Export API key if provided\n\
if [ ! -z "$OPENAI_API_KEY" ]; then\n\
    export OPENAI_API_KEY=$OPENAI_API_KEY\n\
    echo "OpenAI API key configured"\n\
fi\n\
\n\
if [ ! -z "$GOOGLE_API_KEY" ]; then\n\
    export GOOGLE_API_KEY=$GOOGLE_API_KEY\n\
    echo "Google API key configured"\n\
fi\n\
\n\
# Start the application with explicit host binding\n\
echo "Starting CyberScraper 2077..."\n\
streamlit run --server.address 0.0.0.0 --server.port 8501 main.py\n\
' > /app/run.sh

RUN chmod +x /app/run.sh

# Expose only port 8501 for Streamlit (Tor ports are internal only)
EXPOSE 8501

# Set the entrypoint
ENTRYPOINT ["/app/run.sh"]