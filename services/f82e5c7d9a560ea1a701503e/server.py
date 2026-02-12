"""Simple HTTP server using diskcache for demonstration."""
import http.server
import socketserver
import json
from datetime import datetime
from diskcache import Cache

PORT = 8000

# Initialize the disk cache
cache = Cache('/tmp/diskcache-demo')

# Add some cached data
cache['start_time'] = datetime.now().isoformat()
cache['visit_count'] = cache.get('visit_count', 0) + 1


class DiskCacheHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        elif self.path == '/info':
            response = {
                'status': 'running',
                'package': 'diskcache',
                'version': '5.6.3',
                'start_time': cache.get('start_time'),
                'visit_count': cache.get('visit_count'),
                'cache_stats': {
                    'size': len(cache),
                    'volume': cache.volume(),
                }
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response, indent=2).encode())
        else:
            response = {
                'message': 'diskcache library is running',
                'endpoints': ['/health', '/info']
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        pass  # Suppress logging


if __name__ == '__main__':
    with socketserver.TCPServer(('0.0.0.0', PORT), DiskCacheHandler) as httpd:
        print(f'Serving diskcache demo on port {PORT}')
        httpd.serve_forever()