#!/usr/bin/env python3
"""Simple HTTP server to serve Cascadia Code fonts."""

import http.server
import socketserver
import os
from pathlib import Path

PORT = int(os.environ.get("PORT", 8080))
BUILD_DIR = Path("/home/ubuntu/deploy-projects/371e5a0dab254e684d3befe2/build")

class FontHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BUILD_DIR), **kwargs)

    def end_headers(self):
        # Add CORS headers for web font loading
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "public, max-age=86400")
        super().end_headers()

    def guess_type(self, path):
        """Custom MIME types for font files."""
        if path.endswith(".ttf"):
            return "font/ttf"
        elif path.endswith(".otf"):
            return "font/otf"
        elif path.endswith(".woff2"):
            return "font/woff2"
        elif path.endswith(".woff"):
            return "font/woff"
        return super().guess_type(path)

if __name__ == "__main__":
    os.chdir(BUILD_DIR)
    with socketserver.TCPServer(("", PORT), FontHandler) as httpd:
        print(f"Serving fonts at http://0.0.0.0:{PORT}")
        print(f"Build directory: {BUILD_DIR}")
        httpd.serve_forever()