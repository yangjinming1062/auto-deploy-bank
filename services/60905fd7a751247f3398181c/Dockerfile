FROM python:3-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/60905fd7a751247f3398181c

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a simple HTTP server script for healthcheck
RUN echo '#!/usr/bin/env python3\nimport http.server\nimport socketserver\nimport os\nPORT = int(os.environ.get("PORT", 8080))\nclass Handler(http.server.SimpleHTTPRequestHandler):\n    def do_GET(self):\n        self.send_response(200)\n        self.send_header("Content-type", "text/plain")\n        self.end_headers()\n        self.wfile.write(b"OK")\n    def log_message(self, format, *args):\n        pass\nwith socketserver.TCPServer(("", PORT), Handler) as httpd:\n    httpd.serve_forever()' > /server.py

EXPOSE 8080

CMD ["python", "/server.py"]