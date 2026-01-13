# Dockerfile for Softlearning
FROM python:3.8-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV LD_LIBRARY_PATH=/usr/lib/nvidia-000:${LD_LIBRARY_PATH}

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    wget \
    bzip2 \
    unzip \
    ca-certificates \
    git \
    mercurial \
    subversion \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    libglfw3 \
    libglfw3-dev \
    libxrandr2 \
    libxinerama-dev \
    libxi6 \
    libxcursor-dev \
    libgl1-mesa-dev \
    libgl1-mesa-glx \
    libglew-dev \
    libosmesa6-dev \
    lsb-release \
    patchelf \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Set up MuJoCo directories and download binaries
RUN mkdir -p /root/.mujoco && \
    cd /root/.mujoco && \
    wget -q https://www.roboti.us/download/mujoco200_linux.zip -O mujoco200_linux.zip && \
    unzip -q mujoco200_linux.zip && \
    rm mujoco200_linux.zip

# Copy requirements.txt
COPY requirements.txt /tmp/requirements.txt

# Create custom requirements with compatible versions
RUN pip install --no-cache-dir --upgrade pip==24.0 && \
    grep -v "^conda" /tmp/requirements.txt | \
    sed 's/gym==0.18.0/gym==0.17.2/' | \
    sed 's/mujoco-py==2.0.2.13/mujoco-py==2.0.2.10/' | \
    sed 's/cloudpickle==1.6.0/cloudpickle==1.3.0/' > /tmp/requirements_compatible.txt && \
    pip install --no-cache-dir -r /tmp/requirements_compatible.txt

# Copy source code
COPY . /app
WORKDIR /app

# Install the package in development mode
RUN pip install -e .

# Install Flask for web dashboard
RUN pip install --no-cache-dir flask==2.3.3

# Set up MuJoCo environment
ENV LD_LIBRARY_PATH /root/.mujoco/mjpro150/bin:${LD_LIBRARY_PATH}
ENV LD_LIBRARY_PATH /root/.mujoco/mujoco200/bin:${LD_LIBRARY_PATH}
ENV LD_LIBRARY_PATH /root/.mujoco/mujoco200_linux/bin:${LD_LIBRARY_PATH}
ENV LD_LIBRARY_PATH /root/.mujoco/bin:${LD_LIBRARY_PATH}

# Healthcheck - check if the main process is running
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD pgrep -f "softlearning run_example_local" || exit 1

# Run the web server
CMD ["python", "web_server.py"]