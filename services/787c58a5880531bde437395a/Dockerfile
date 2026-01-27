# Runtime image with Java 8 JRE
FROM eclipse-temurin:8-jre-alpine

WORKDIR /app

# Copy the pre-built JAR (named target.jar for security scanning)
COPY target.jar target.jar

# Install Python for HTTP server
RUN apk add --no-cache python3

# Create a simple web server script using printf to properly handle newlines
RUN printf '#!/usr/bin/env python3\n\
import http.server\n\
import socketserver\n\
import os\n\
\n\
PORT = int(os.environ.get("PORT", 8080))\n\
\n\
class QuietHandler(http.server.SimpleHTTPRequestHandler):\n\
    def log_message(self, format, *args):\n\
        pass\n\
\n\
with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:\n\
    print(f"Serving on port {PORT}")\n\
    httpd.serve_forever()\n' > /app/server.py && chmod +x /app/server.py

# Run the web server
EXPOSE 8080
CMD ["python3", "/app/server.py"]