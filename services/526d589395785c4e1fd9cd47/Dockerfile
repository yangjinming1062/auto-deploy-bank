FROM python:3.9-slim

# Install curl, protoc, and other dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Protocol Buffer compiler (protoc)
ARG PROTOC_VERSION=25.2
RUN wget -q https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOC_VERSION}/protoc-${PROTOC_VERSION}-linux-x86_64.zip \
    && unzip -o protoc-${PROTOC_VERSION}-linux-x86_64.zip -d /usr/local \
    && rm protoc-${PROTOC_VERSION}-linux-x86_64.zip

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PROTOC=/usr/local/bin/protoc

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/526d589395785c4e1fd9cd47

# Copy all source files needed for setup.py
COPY setup.py .
COPY README.md .
COPY MANIFEST.in .
COPY requirements-docs.txt .
COPY tensorflow_model_analysis/ tensorflow_model_analysis/

# Install the package (dependencies are defined in setup.py)
RUN pip install --no-cache-dir .

# Default command - simple HTTP server for healthchecks
CMD ["python", "-c", "\
import http.server\n\
import socketserver\n\
\n\
class HealthHandler(http.server.BaseHTTPRequestHandler):\n\
    def do_GET(self):\n\
        if self.path == '/health':\n\
            try:\n\
                import tensorflow_model_analysis\n\
                self.send_response(200)\n\
                self.send_header('Content-type', 'text/plain')\n\
                self.end_headers()\n\
                self.wfile.write(b'OK')\n\
            except Exception as e:\n\
                self.send_response(500)\n\
                self.send_header('Content-type', 'text/plain')\n\
                self.end_headers()\n\
                self.wfile.write(f'ERROR: {e}'.encode())\n\
        else:\n\
            self.send_response(404)\n\
            self.end_headers()\n\
\n\
    def log_message(self, format, *args):\n\
        pass  # Suppress logging\n\
\n\
with socketserver.TCPServer(('0.0.0.0', 48821), HealthHandler) as httpd:\n\
    httpd.serve_forever()\n"]