FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libtiff5-dev \
    libopenjp2-7-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/9be15d1c8e6bc50b7189568c

# Copy all source files needed for building Pillow
COPY setup.py pyproject.toml ./
COPY _custom_build ./_custom_build
COPY src/PIL ./src/PIL
COPY src/libImaging ./src/libImaging
COPY src/Tk ./src/Tk
COPY src/thirdparty ./src/thirdparty
COPY src/*.c src/*.h src/ ./src/

# Install Pillow from source
RUN pip install --no-cache-dir .

# Copy remaining files
COPY . .

# Copy healthcheck script
COPY --chmod=755 <<'EOF' /healthcheck.py
#!/usr/bin/env python3
"""Simple health check server for Pillow container."""
import http.server
import socketserver
import os
import subprocess

PORT = int(os.environ.get("PORT", 8080))

class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health" or self.path == "/":
            # Check if Pillow is properly installed
            try:
                from PIL import Image, features
                # Verify core is available by accessing it
                _ = Image.core
                # Get version info as additional check
                version = Image.__version__
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(f"Pillow is healthy (version: {version})".encode())
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(f"Pillow error: {e}".encode())
        elif self.path == "/selftest":
            # Run selftest
            try:
                result = subprocess.run(
                    ["python", "selftest.py"],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                self.send_response(200 if result.returncode == 0 else 500)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(result.stdout.encode())
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(f"Selftest error: {e}".encode())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not found")

    def log_message(self, format, *args):
        pass  # Suppress logging

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), HealthHandler) as httpd:
        print(f"Health server running on port {PORT}")
        httpd.serve_forever()
EOF

RUN chmod +x /healthcheck.py

EXPOSE 8080

CMD ["python", "/healthcheck.py"]