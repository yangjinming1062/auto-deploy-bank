#!/usr/bin/env python3
"""
Simple HTTP server for D-NeRF Training Service status page.
Provides health checks and service information.
"""

import http.server
import json
import os
import socketserver
from datetime import datetime

PORT = 8000

class DNeRFStatusHandler(http.server.BaseHTTPRequestHandler):
    """Custom handler for D-NeRF service status page."""

    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/' or self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_status_page().encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'service': 'dnerf-training-service',
                'timestamp': datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/api/info':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'service': 'D-NeRF Training Service',
                'version': '1.0.0',
                'description': 'Dynamic Neural Radiance Fields Training',
                'environment': {
                    'PYTHONPATH': os.environ.get('PYTHONPATH', ''),
                    'D_NERF_BASEDIR': os.environ.get('D_NERF_BASEDIR', ''),
                    'D_NERF_DATADIR': os.environ.get('D_NERF_DATADIR', ''),
                },
                'data_directory': os.listdir('/home/ubuntu/deploy-projects/1d975e07b1e87c514c26a788/data') if os.path.exists('/home/ubuntu/deploy-projects/1d975e07b1e87c514c26a788/data') else [],
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Not found'}
            self.wfile.write(json.dumps(response).encode())

    def get_status_page(self):
        """Generate the HTML status page."""
        data_dir = '/home/ubuntu/deploy-projects/1d975e07b1e87c514c26a788/data'
        data_exists = os.path.exists(data_dir)
        data_contents = os.listdir(data_dir) if data_exists else []

        return f"""<!DOCTYPE html>
<html>
<head>
    <title>D-NeRF Training Service</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }}
        .status {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .healthy {{
            background: #28a745;
            color: white;
        }}
        .info {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin: 10px 0;
        }}
        .api-links {{
            margin-top: 20px;
        }}
        .api-links a {{
            display: inline-block;
            margin-right: 15px;
            color: #007bff;
            text-decoration: none;
        }}
        .api-links a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>D-NeRF Training Service</h1>
        <div class="status healthy">Service Status: Healthy</div>

        <div class="info">
            <p><strong>Service:</strong> Dynamic Neural Radiance Fields Training</p>
            <p><strong>Started:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Port:</strong> {PORT}</p>
        </div>

        <h2>Environment</h2>
        <div class="info">
            <p><strong>Data Directory:</strong> /home/ubuntu/deploy-projects/1d975e07b1e87c514c26a788/data</p>
            <p><strong>Data Present:</strong> {'Yes' if data_contents else 'No'}</p>
            {'<p><strong>Datasets:</strong> ' + ', '.join(data_contents) + '</p>' if data_contents else ''}
        </div>

        <h2>Available API Endpoints</h2>
        <div class="api-links">
            <a href="/health">/health</a>
            <a href="/api/info">/api/info</a>
        </div>
    </div>
</body>
</html>"""

    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {args[0]}")

def main():
    """Start the HTTP server."""
    with socketserver.TCPServer(("", PORT), DNeRFStatusHandler) as httpd:
        print(f"D-NeRF Training Service Status Server running on port {PORT}")
        print(f"Access the status page at http://localhost:{PORT}")
        print("Available endpoints:")
        print(f"  - GET /       (HTML status page)")
        print(f"  - GET /health (JSON health check)")
        print(f"  - GET /api/info (JSON service info)")
        httpd.serve_forever()

if __name__ == "__main__":
    main()