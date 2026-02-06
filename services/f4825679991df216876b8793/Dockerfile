FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install system dependencies for wxPython and Xvfb
RUN apt-get update && apt-get install -y \
    xvfb \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libx11-6 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxcursor1 \
    libxcomposite1 \
    libxdamage1 \
    libxshmfence1 \
    libxxf86vm1 \
    libfontconfig1 \
    libfreetype6 \
    libasound2 \
    curl \
    build-essential \
    libgtk-3-dev \
    libnotify-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/f4825679991df216876b8793

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make start script executable
RUN chmod +x /home/ubuntu/deploy-projects/f4825679991df216876b8793/start.sh

# Expose HTTP port
EXPOSE 8080

# Healthcheck using curl
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the HTTP server for headless mode
CMD ["python", "http_server.py"]