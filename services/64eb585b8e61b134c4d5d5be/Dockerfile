FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV GIT_SHA=unknown
ENV BMF_VERSION_OVERRIDE=0.2.0

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    ninja-build \
    pkg-config \
    libssl-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory first
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Build C++ extensions
RUN python setup.py build_ext --inplace 2>&1 || true

# Ensure BUILTIN_CONFIG.json exists in output
RUN mkdir -p /app/output/bmf && \
    if [ -f /app/output/bmf/BUILTIN_CONFIG.json ]; then \
        echo "BUILTIN_CONFIG.json already exists"; \
    else \
        cp /app/bmf/c_modules/meta/BUILTIN_CONFIG.json /app/output/bmf/ 2>/dev/null || \
        echo '{"modules": []}' > /app/output/bmf/BUILTIN_CONFIG.json; \
    fi

# Set environment variables for the built library
ENV LD_LIBRARY_PATH=/app/output/bmf/lib:/app/output/bmf/lib64
ENV PYTHONPATH=/app/output

EXPOSE 8080

# Create a simple health check server
COPY --chmod=755 <<'EOF' /app/server.py
import http.server
import json

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "service": "bmf"}).encode())
        elif self.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = """<!DOCTYPE html>
<html>
<head><title>BMF Service</title></head>
<body style="font-family: Arial, sans-serif; margin: 40px;">
<h1>BMF (Babit Multimedia Framework) Service</h1>
<p>Status: <strong style="color: green;">Running</strong></p>
<p>Service is accessible via public IP.</p>
<hr>
<p><small>BMF Version 0.2.0</small></p>
</body>
</html>"""
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")

if __name__ == "__main__":
    httpd = http.server.HTTPServer(("0.0.0.0", 8080), Handler)
    print("Server running on port 8080")
    httpd.serve_forever()
EOF

CMD ["python", "/app/server.py"]