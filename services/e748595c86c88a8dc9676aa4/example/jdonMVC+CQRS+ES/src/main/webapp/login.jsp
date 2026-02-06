<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
    String error = "";
    String username = request.getParameter("username");
    String password = request.getParameter("password");

    if (username != null && password != null) {
        // Validate credentials
        if ("admin".equals(username) && "Admin@123".equals(password)) {
            session.setAttribute("user", username);
            session.setAttribute("role", "admin");
            response.sendRedirect("index.jsp");
            return;
        } else if ("user1".equals(username) && "User@123".equals(password)) {
            session.setAttribute("user", username);
            session.setAttribute("role", "normal");
            response.sendRedirect("index.jsp");
            return;
        } else {
            error = "Invalid username or password";
        }
    }

    // Logout functionality
    String action = request.getParameter("action");
    if ("logout".equals(action)) {
        session.invalidate();
        response.sendRedirect("login.jsp");
        return;
    }
%>
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Login - JdonMVC Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background: white;
            padding: 30px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            width: 300px;
        }
        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 3px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            width: 100%;
            padding: 10px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            margin-top: 10px;
        }
        input[type="submit"]:hover {
            background: #0056b3;
        }
        .error {
            color: red;
            font-size: 14px;
            text-align: center;
            margin-bottom: 15px;
        }
        .info {
            font-size: 12px;
            color: #666;
            margin-top: 15px;
            padding: 10px;
            background: #f9f9f9;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Login</h2>
        <% if (!error.isEmpty()) { %>
            <div class="error"><%= error %></div>
        <% } %>
        <form method="post">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <input type="submit" value="Login">
        </form>
        <div class="info">
            <strong>Demo Credentials:</strong><br>
            Admin: admin / Admin@123<br>
            User: user1 / User@123
        </div>
    </div>
</body>
</html>