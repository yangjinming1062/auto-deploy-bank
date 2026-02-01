FROM python:3.11-slim

# Install system dependencies for Tkinter, Xvfb, and basic X11
RUN apt-get update && apt-get install -y \
    curl \
    xvfb \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/da465666a1ae29be5e3a2fc7

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Expose port for web interface
EXPOSE 40341

# Run the startup script
CMD ["./start.sh"]