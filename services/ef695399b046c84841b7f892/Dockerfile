FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/ef695399b046c84841b7f892

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/home/ubuntu/deploy-projects/ef695399b046c84841b7f892

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a simple health check endpoint
RUN cat > /home/ubuntu/deploy-projects/ef695399b046c84841b7f892/health_server.py << 'EOF'
import http.server
import socketserver
import threading

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress logging

PORT = 8080

with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
    print(f"Server running on port {PORT}")
    httpd.serve_forever()
EOF

# Expose internal port (will be overridden by docker-compose)
EXPOSE 8080

# Run health server in foreground
CMD ["python", "/home/ubuntu/deploy-projects/ef695399b046c84841b7f892/health_server.py"]