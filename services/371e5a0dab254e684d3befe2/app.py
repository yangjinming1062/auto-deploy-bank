#!/usr/bin/env python3
"""Simple HTTP server for Cascadia Code font build service."""

import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 8080))


class HealthHandler(http.server.BaseHTTPRequestHandler):
    """Simple handler that returns 200 OK for health checks."""

    def do_GET(self):
        if self.path in("/", "/health", "/healthz"):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK - Cascadia Code Font Build Service")
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), HealthHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()