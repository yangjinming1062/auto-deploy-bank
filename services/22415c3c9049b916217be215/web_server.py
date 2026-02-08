#!/usr/bin/env python3
"""Simple HTTP status server for train ticket bot"""
import http.server
import socketserver
import os
import subprocess
import json
from datetime import datetime

PORT = int(os.environ.get("WEB_PORT", 8080))

class StatusHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health" or self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            # Get container status
            status = "running"
            try:
                result = subprocess.run(
                    ["ps", "aux"],
                    capture_output=True,
                    text=True
                )
                has_bot = "fuckeverything.py" in result.stdout
                status = "running" if has_bot else "stopped"
            except:
                status = "unknown"

            response = {
                "service": "train-ticket-bot",
                "status": status,
                "timestamp": datetime.now().isoformat(),
                "port": PORT,
                "message": "Train ticket automation bot is running"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')

    def log_message(self, format, *args):
        print(f"[Web] {args[0]}")

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), StatusHandler) as httpd:
        print(f"Status server running on port {PORT}")
        httpd.serve_forever()