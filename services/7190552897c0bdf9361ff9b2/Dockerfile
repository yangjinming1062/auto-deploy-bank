FROM python:3.8-slim

# Install curl for healthcheck and build dependencies for scipy
RUN apt-get update && apt-get install -y \
    curl \
    libopenblas-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/7190552897c0bdf9361ff9b2

# Install PyTorch CPU-only first (smaller, no CUDA dependencies)
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Copy requirements.txt (without torch/torchvision since already installed)
COPY requirements.txt /tmp/requirements.txt
# Install remaining dependencies - use flexible versions for compatibility
RUN cat /tmp/requirements.txt | tr -d '\r' | grep -v '^torch$' | grep -v '^torchvision$' > requirements.txt && \
    pip install --no-cache-dir tensorboard scikit-learn scipy numpy matplotlib opencv-python tqdm Pillow h5py

# Copy application code
COPY . .

# Create entrypoint.py directly
RUN cat > /home/ubuntu/deploy-projects/7190552897c0bdf9361ff9b2/entrypoint.py << 'ENTRYPOINT_EOF'
#!/usr/bin/env python3
import os
import sys
import threading
import time

MODE = os.environ.get("MODE", "train")
PORT = int(os.environ.get("PORT", 40200))
ANNOTATION_PATH = "cls_train.txt"

def run_http_server():
    """Run a simple HTTP server for healthcheck/status."""
    import http.server
    import socketserver
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/health" or self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"FaceNet Service Running")
            else:
                self.send_response(404)
                self.end_headers()
        def log_message(self, format, *args):
            pass  # Suppress logging

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"HTTP server running on port {PORT} for healthcheck")
        httpd.serve_forever()

def run_train():
    """Run training only if annotation file exists, otherwise keep container alive."""
    if not os.path.exists(ANNOTATION_PATH):
        print(f"Annotation file {ANNOTATION_PATH} not found.")
        print("Container will stay running. Prepare dataset and run txt_annotation.py to generate it.")
        # Keep container alive - HTTP server thread handles healthcheck
        while True:
            time.sleep(3600)

    print("Annotation file found, starting training...")
    # Run training and exit with its return code
    sys.exit(os.system("python train.py"))

def run_predict():
    """Run face prediction."""
    print("Starting face prediction mode...")
    sys.exit(os.system("python predict.py"))

def run_eval():
    """Run LFW evaluation."""
    print("Starting LFW evaluation mode...")
    sys.exit(os.system("python eval_LFW.py"))

if __name__ == "__main__":
    # Start HTTP server in a separate thread for healthcheck
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()

    # Run main application based on MODE
    if MODE == "predict":
        run_predict()
    elif MODE == "eval":
        run_eval()
    else:
        run_train()
ENTRYPOINT_EOF

RUN chmod +x /home/ubuntu/deploy-projects/7190552897c0bdf9361ff9b2/entrypoint.py

EXPOSE 40200

CMD ["python", "entrypoint.py"]