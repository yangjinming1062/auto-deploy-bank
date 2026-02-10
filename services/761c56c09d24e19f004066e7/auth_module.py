"""
Bokeh Server Authentication Module for Security Testing

This is a demonstration auth module for testing purposes only.
It provides simple cookie-based authentication with test accounts.

WARNING: This module is for testing only. Do not use in production.
"""

import tornado
from tornado.web import RequestHandler

# User database - demo accounts for security testing
USERS = {
    "admin": {
        "password": "Admin@123",
        "role": "admin",
        "permissions": ["read", "write", "delete", "admin"]
    },
    "user": {
        "password": "User@123",
        "role": "normal",
        "permissions": ["read"]
    }
}

def get_user(request_handler):
    """Get the current authenticated user from cookie."""
    import base64
    cookie_value = request_handler.get_cookie("user")
    if cookie_value:
        try:
            return base64.b64decode(cookie_value.encode()).decode()
        except Exception:
            return None
    return None

# could also define get_login_url function (but must give up LoginHandler)
login_url = "/login"

class LoginHandler(RequestHandler):
    """Handler for user login."""

    def get(self):
        try:
            errormessage = self.get_argument("error")
        except Exception:
            errormessage = ""
        self.render("templates/login.html", errormessage=errormessage)

    def check_permission(self, username, password):
        """Check if username/password combination is valid."""
        if username in USERS and USERS[username]["password"] == password:
            return True
        return False

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        auth = self.check_permission(username, password)
        if auth:
            self.set_current_user(username)
            self.redirect("/")
        else:
            error_msg = "?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect(login_url + error_msg)

    def set_current_user(self, user):
        if user:
            user_data = {
                "username": user,
                "role": USERS[user]["role"],
                "permissions": USERS[user]["permissions"]
            }
            # Use base64 encoding to avoid cookie value issues with special characters
            import base64
            encoded_value = base64.b64encode(tornado.escape.json_encode(user_data).encode()).decode()
            self.set_cookie("user", encoded_value, httponly=True)
        else:
            self.clear_cookie("user")

logout_url = "/logout"

class LogoutHandler(RequestHandler):
    """Handler for user logout."""

    def get(self):
        self.clear_cookie("user")
        self.redirect("/")