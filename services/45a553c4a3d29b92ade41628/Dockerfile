FROM python:3.10-slim-bookworm

# Install curl for healthcheck and OpenGL/X11 dependencies for OpenCV headless
RUN apt-get update && apt-get install -y \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxcb1 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:0
ENV QT_QPA_PLATFORM=offscreen

WORKDIR /home/ubuntu/deploy-projects/45a553c4a3d29b92ade41628

# Copy requirements first for better layer caching
COPY Requirements.txt .
RUN pip install --no-cache-dir -r Requirements.txt

# Copy application code
COPY . .

# Make startup script executable
RUN chmod +x start.sh

# Default command - run the sky replacement tool via startup script
CMD ["./start.sh"]