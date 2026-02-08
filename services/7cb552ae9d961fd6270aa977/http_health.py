#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect(('rpc-provider', 8080))
            sock.send(b'ping')
            sock.recv(1024)
            sock.close()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "healthy", "service": "rpc-provider"}')
        except Exception as e:
            self.send_response(503)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def log_message(self, format, *args):
        pass


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8081), HealthHandler)
    print('HTTP health check server running on port 8081')
    server.serve_forever()