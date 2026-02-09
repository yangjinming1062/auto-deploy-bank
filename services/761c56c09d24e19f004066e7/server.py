#!/usr/bin/env python
"""Login server with embedded Bokeh proxy."""
import os
import sys
import subprocess
import time
import urllib.request

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from tornado.httpserver import HTTPServer

# Credentials for authentication
VALID_USERS = {
    "admin": ("admin", "Admin@123"),
    "normal": ("normal", "User@123"),
}


class LoginHandler(RequestHandler):
    """Serve login page and handle login POST."""

    def get(self):
        errormessage = self.get_argument("error", "")
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "login.html")
        with open(template_path, 'r') as f:
            template = f.read()
        template = template.replace('{{errormessage}}', errormessage)
        template = template.replace('{% module xsrf_form_html() %}', '')
        self.write(template)

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")

        # Check credentials
        if username in VALID_USERS and VALID_USERS[username][1] == password:
            role = username  # admin or normal
            self.set_cookie("user", role, path="/")
            self.redirect("/")
        else:
            self.redirect("/login?error=Login+incorrect")


class LogoutHandler(RequestHandler):
    """Handle logout."""

    def get(self):
        self.clear_cookie("user", path="/")
        self.redirect("/login")


class BokehProxyHandler(RequestHandler):
    """Proxy requests to Bokeh server."""

    async def get(self, path=None):
        query = self.request.query

        # Build the URL to proxy to (Bokeh runs on port 5007 internally)
        bokeh_url = "http://127.0.0.1:5007"
        if path:
            url = f"{bokeh_url}/{path}"
        else:
            url = bokeh_url
        if query:
            url += f"?{query}"

        try:
            req = urllib.request.Request(url)
            req.add_header('Host', self.request.host)
            response = urllib.request.urlopen(req, timeout=10)
            self.set_status(response.getcode())
            self.write(response.read())
        except Exception as e:
            self.set_status(502)
            self.write(f"Proxy error: {e}")

    async def post(self, path=None):
        query = self.request.query

        # Build the URL to proxy to (Bokeh runs on port 5007 internally)
        bokeh_url = "http://127.0.0.1:5007"
        if path:
            url = f"{bokeh_url}/{path}"
        else:
            url = bokeh_url
        if query:
            url += f"?{query}"

        try:
            body = self.request.body.decode('utf-8') if self.request.body else ""
            req = urllib.request.Request(url, data=body.encode('utf-8'))
            req.add_header('Host', self.request.host)
            req.add_header('Content-Type', self.request.headers.get('Content-Type', 'application/x-www-form-urlencoded'))
            response = urllib.request.urlopen(req, timeout=10)
            self.set_status(response.getcode())
            self.write(response.read())
        except Exception as e:
            self.set_status(502)
            self.write(f"Proxy error: {e}")


def start_bokeh_server():
    """Start the Bokeh server using subprocess."""
    app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")

    # Start Bokeh server as subprocess - redirect output to /dev/null
    print(f"Starting Bokeh server on port 5007...", file=sys.stderr)
    with open(os.devnull, 'wb') as devnull:
        bokeh_proc = subprocess.Popen(
            [sys.executable, "-m", "bokeh", "serve", app_dir, "--port", "5007", "--address", "127.0.0.1", "--allow-websocket-origin", "*"],
            stdin=subprocess.PIPE,
            stdout=devnull,
            stderr=devnull,
        )
    print(f"Bokeh server process started with PID: {bokeh_proc.pid}", file=sys.stderr)
    return bokeh_proc


def make_app():
    """Create the Tornado application."""
    return Application([
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/(.*)", BokehProxyHandler),
    ])


def main():
    """Run the servers."""
    # Start Bokeh server as subprocess
    bokeh_proc = start_bokeh_server()

    # Wait for Bokeh server to start
    time.sleep(5)

    # Start the login/proxy server
    app = make_app()
    server = HTTPServer(app)
    server.listen(5006, address="0.0.0.0")
    print("Server started on http://0.0.0.0:5006", file=sys.stderr)
    IOLoop.current().start()


if __name__ == "__main__":
    main()