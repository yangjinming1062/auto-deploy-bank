#!/usr/bin/env python3
"""Simple HTTP server for Deep Snake Training container."""

import http.server
import socketserver
import os
import datetime

PORT = int(os.environ.get('PORT', 8080))

class SnakeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Deep Snake Training</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a2e; color: #eee; }}
        h1 {{ color: #00d9ff; }}
        .status {{ background: #16213e; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .ok {{ color: #00ff88; }}
        .info {{ color: #ffcc00; }}
    </style>
</head>
<body>
    <h1>Deep Snake Training Container</h1>
    <div class="status">
        <p class="ok">Status: Container Running</p>
        <p class="info">Server: Python HTTP Server</p>
        <p>Port: {PORT}</p>
        <p>Time: {datetime.datetime.now().isoformat()}</p>
    </div>
    <p>CUDA_HOME: {os.environ.get('CUDA_HOME', 'not set')}</p>
    <p>FORCE_CUDA: {os.environ.get('FORCE_CUDA', '0')}</p>
</body>
</html>"""
            self.wfile.write(html.encode())
        else:
            super().do_GET()

    def log_message(self, format, *args):
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {args[0]}")

if __name__ == '__main__':
    print(f"Starting web server on port {PORT}...")
    with socketserver.TCPServer(("", PORT), SnakeHTTPRequestHandler) as httpd:
        print(f"Serving at http://0.0.0.0:{PORT}")
        httpd.serve_forever()