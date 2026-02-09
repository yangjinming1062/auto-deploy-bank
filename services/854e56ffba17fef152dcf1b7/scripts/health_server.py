#!/usr/bin/env python
"""Simple HTTP health check server for Poutyne container."""
import http.server
import json
import socketserver
import sys
import poutyne

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080


class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'package': 'poutyne',
                'version': poutyne.__version__
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress logging


if __name__ == '__main__':
    print(f"Poutyne health server starting on port {PORT}")
    with socketserver.TCPServer(("", PORT), HealthHandler) as httpd:
        httpd.serve_forever()