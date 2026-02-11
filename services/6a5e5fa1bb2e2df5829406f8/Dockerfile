FROM python:3.12-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install maturin for building Rust/Python extension
RUN pip install --no-cache-dir "maturin>=1.9.4,<2"

WORKDIR /home/ubuntu/deploy-projects/6a5e5fa1bb2e2df5829406f8

# Copy project files for building
COPY pyproject.toml .
COPY README.rst .
COPY LICENSE LICENSE.APACHE LICENSE.BSD ./
COPY CONTRIBUTING.rst .
COPY Cargo.toml Cargo.lock ./
COPY src src
COPY release.py .

# Build and install the cryptography library
RUN pip install --no-cache-dir .

# Final stage - minimal runtime image
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/6a5e5fa1bb2e2df5829406f8

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application files
COPY --from=builder /home/ubuntu/deploy-projects/6a5e5fa1bb2e2df5829406f8 /home/ubuntu/deploy-projects/6a5e5fa1bb2e2df5829406f8

# Create a simple HTTP server script
COPY <<'EOF' /home/ubuntu/deploy-projects/6a5e5fa1bb2e2df5829406f8/server.py
#!/usr/bin/env python3
"""Simple HTTP server to verify cryptography library is installed."""
import http.server
import socketserver
import json
import cryptography

PORT = 8000

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {
            "status": "ok",
            "library": "cryptography",
            "version": cryptography.__version__
        }
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        pass  # Suppress logging

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()
EOF

RUN chmod +x /home/ubuntu/deploy-projects/6a5e5fa1bb2e2df5829406f8/server.py

EXPOSE 8000

CMD ["python", "server.py"]