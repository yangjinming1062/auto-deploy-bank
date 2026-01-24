FROM python:3.9-slim

# Install system dependencies for Qt5, Xvfb, and OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libxext6 \
    libxrender1 \
    xvfb \
    libsm6 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libfontconfig1 \
    libfreetype6 \
    libxcb1 \
    libxcb-shm0 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libxcb-render0 \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxkbcommon0 \
    libxkbcommon-x11-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libasound2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV GIT_PYTHON_REFRESH=quiet
ENV DISPLAY=:99

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/1cff50108f7225c7819467f6

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (for potential future web interface, not used by current app)
EXPOSE 51414

# Run Flask web server
CMD ["python", "web_server.py"]