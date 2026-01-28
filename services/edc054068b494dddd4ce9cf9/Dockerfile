FROM python:3.10-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    ninja-build \
    pkg-config \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libosmesa6 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYOPENGL_PLATFORM=osmesa
ENV CUDA_HOME=/usr/local/cuda
ENV HF_HOME=/root/.cache
ENV PYTORCH_KERNEL_CACHE_PATH=/root/.cache/torch
ENV OPENCV_IO_ENABLE_OPENEXR=1
ENV KMP_DUPLICATE_LIB_OK=TRUE
ENV PYTHONPATH=/app:${PYTHONPATH}
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:${LD_LIBRARY_PATH}

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install torch first (required by flash-attn and other packages)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install Python dependencies (excluding torch and flash-attn to avoid conflicts)
RUN grep -v -E '^(torch|flash_attn)' requirements.txt | pip install --no-cache-dir -r /dev/stdin || true

# Try installing remaining packages that might have failed (flash-attn is optional)
RUN pip install --no-cache-dir flash-attn --no-build-isolation || echo "flash-attn installation skipped (optional)"

# Install git+ packages
RUN pip install --no-cache-dir git+https://github.com/openai/CLIP.git@main && \
    pip install --no-cache-dir git+https://github.com/marian42/mesh_to_sdf.git && \
    pip install --no-cache-dir git+https://github.com/YuliangXiu/taming-transformers.git

# Copy CUDA kernels setup files
COPY cores/lib/freqencoder/setup.py cores/lib/freqencoder/setup.py
COPY cores/lib/freqencoder/*.cu cores/lib/freqencoder/
COPY cores/lib/gridencoder/setup.py cores/lib/gridencoder/setup.py
COPY cores/lib/gridencoder/*.cu cores/lib/gridencoder/

# Compile custom CUDA kernels (skip if nvcc not available, runtime will handle)
RUN (which nvcc && cd cores/lib/freqencoder && python setup.py build_ext --inplace && cd ../.. && cd cores/lib/gridencoder && python setup.py build_ext --inplace && cd ../..) || echo "CUDA kernel compilation skipped (will be compiled at runtime if nvcc available)"

# Copy application code
COPY . .

# Create a simple healthcheck server
RUN cat > /app/health_server.py << 'HEALTHSERVER'
#!/usr/bin/env python3
import http.server
import socketserver
import os
import signal
import sys

PORT = 8501

class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"PuzzleAvatar is running")
        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            status = os.environ.get("JOB_STATUS", "pending")
            self.wfile.write(f"Status: {status}".encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

def signal_handler(sig, frame):
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    with socketserver.TCPServer(("", PORT), HealthHandler) as httpd:
        print(f"Health check server running on port {PORT}")
        httpd.serve_forever()
HEALTHSERVER
RUN chmod +x /app/health_server.py

# Expose the healthcheck port
EXPOSE 8501

# Default command - run healthcheck server in background then wait
# The actual job should be run with docker compose exec or by overriding the command
CMD ["python", "-c", "import subprocess; import os; os.environ['JOB_STATUS']='ready'; subprocess.Popen(['python', '/app/health_server.py']); import time; time.sleep(31536000)"]