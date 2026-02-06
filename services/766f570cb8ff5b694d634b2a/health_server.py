#!/usr/bin/env python
"""Simple HTTP health server."""

import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 8080))


class HealthHandler(http.server.SimpleHTTPRequestHandler):
    """Handler that returns health status."""

    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/health" or self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "healthy"}')
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "not found"}')

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), HealthHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()