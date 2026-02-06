#!/usr/bin/env python3
"""
Wrapper script that runs both gRPC FlightServer (via subprocess) and HTTP health endpoint
"""
import sys
import os
import socket
import subprocess
import signal

# Add project root to Python path
sys.path.insert(0, '/home/ubuntu/deploy-projects/66995efbaed073388e2eae8d')

import threading
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# gRPC server process
grpc_process = None

def check_grpc_available(host='localhost', port=5005, timeout=2):
    """Check if gRPC port is available/responding"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def start_grpc_server():
    """Start the gRPC FlightServer as a subprocess"""
    global grpc_process
    try:
        print("Starting gRPC FlightServer subprocess on 0.0.0.0:5005...")
        # Run the gRPC server as a separate Python process
        grpc_process = subprocess.Popen(
            [sys.executable, '-c',
             'from pyquokka.flight import FlightServer; '
             's = FlightServer("0.0.0.0", location="grpc+tcp://0.0.0.0:5005"); '
             's.serve()'],
            cwd='/home/ubuntu/deploy-projects/66995efbaed073388e2eae8d',
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        print(f"gRPC server started with PID {grpc_process.pid}")
    except Exception as e:
        print(f"Warning: Could not start gRPC server: {e}")

class HealthHandler(BaseHTTPRequestHandler):
    """HTTP handler for health checks and service info"""

    def do_GET(self):
        if self.path == "/" or self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            grpc_healthy = check_grpc_available()

            response = {
                "status": "healthy" if grpc_healthy else "degraded",
                "service": "pyquokka-flight-server",
                "grpc_available": grpc_healthy,
                "grpc_port": 5005,
                "http_port": 5006,
                "endpoints": {
                    "grpc": "grpc://host:40567",
                    "health": "http://host:40568/health"
                },
                "message": "PyQuokka Arrow Flight server is running"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        elif self.path == "/grpc":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "endpoint": "grpc://host:40567",
                "description": "PyQuokka Arrow Flight gRPC server",
                "port_mapping": {
                    "host": 40567,
                    "container": 5005
                }
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found", "available_paths": ["/health", "/grpc"]}).encode())

    def log_message(self, format, *args):
        print(f"[HTTP] {args[0]}")

HTTP_PORT = 5006

def main():
    global grpc_process

    # Start gRPC server in background
    print("Starting gRPC server...")
    start_grpc_server()

    # Wait for gRPC server to start
    print("Waiting for gRPC server to be ready...")
    for i in range(10):
        if check_grpc_available():
            print("gRPC server is ready!")
            break
        time.sleep(1)
    else:
        print("Warning: gRPC server may not be ready yet")

    # Start HTTP server
    http_server = HTTPServer(("0.0.0.0", HTTP_PORT), HealthHandler)
    print(f"HTTP health endpoint started on 0.0.0.0:{HTTP_PORT}")
    print(f"Access health check at: http://0.0.0.0:{HTTP_PORT}/health")

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        if grpc_process:
            grpc_process.terminate()
            grpc_process.wait()
        http_server.shutdown()

if __name__ == "__main__":
    main()