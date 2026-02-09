'''

Bokeh server authentication module for security testing.

This is a modified version of the example auth module with test credentials
for security testing purposes.

Authentication is customizable - you can modify the check_permission function
to implement any authentication flow you require (OAuth, LDAP, database auth, etc.)

'''
import tornado
from tornado.web import RequestHandler


# Get user from cookie - customize this to retrieve user from your auth system
def get_user(request_handler):
    return request_handler.get_cookie("user")


# Login URL path
login_url = "/login"


# Login handler
class LoginHandler(RequestHandler):

    def get(self):
        try:
            errormessage = self.get_argument("error")
        except Exception:
            errormessage = ""
        self.render("login.html", errormessage=errormessage)

    def check_permission(self, username, password):
        '''
        Authentication logic - modify this to implement your auth flow.
        For security testing, we support the following test accounts:
        - admin / Admin@123 (full privileges)
        - normal / User@123 (standard user)
        '''
        # Test credentials for security testing
        if username == "admin" and password == "Admin@123":
            return "admin"
        if username == "normal" and password == "User@123":
            return "normal"
        return False

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        user_role = self.check_permission(username, password)
        if user_role:
            self.set_current_user(user_role)
            self.redirect("/")
        else:
            error_msg = "?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect(login_url + error_msg)

    def set_current_user(self, user):
        if user:
            # Store user role in cookie for session management
            user_data = tornado.escape.json_encode({"username": user})
            self.set_cookie("user", user_data)
        else:
            self.clear_cookie("user")


# Logout URL path
logout_url = "/logout"


# Logout handler
class LogoutHandler(RequestHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect("/")