package com.myblog.controller;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;
import java.io.PrintWriter;

/**
 * Simple login servlet for external Tomcat deployment
 * Works when Spring Boot context doesn't initialize
 */
@WebServlet(urlPatterns = {"/public/login.do", "/login"})
public class LoginServlet extends HttpServlet {

    // Demo credentials
    private static final String ADMIN_USER = "root";
    private static final String ADMIN_PASS = "Admin@123";
    private static final String NORMAL_USER = "testuser";
    private static final String NORMAL_PASS = "User@123";

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("application/json;charset=UTF-8");
        response.setCharacterEncoding("UTF-8");
        PrintWriter out = response.getWriter();

        String account = request.getParameter("account");
        String password = request.getParameter("password");
        String source = request.getParameter("source");

        if (ADMIN_USER.equals(account) && ADMIN_PASS.equals(password)) {
            // Admin login successful
            HttpSession session = request.getSession(true);
            session.setAttribute("userRole", "admin");
            session.setAttribute("username", account);
            session.setAttribute("loggedIn", true);

            // Set cookies for session
            response.addCookie(createCookie("userRole", "admin", 3600));
            response.addCookie(createCookie("username", account, 3600));
            response.addCookie(createCookie("loggedIn", "true", 3600));

            out.print("{\"success\":true,\"message\":\"登录成功\",\"userRole\":\"admin\",\"username\":\"" + account + "\"}");
        } else if (NORMAL_USER.equals(account) && NORMAL_PASS.equals(password)) {
            // Normal user login successful
            HttpSession session = request.getSession(true);
            session.setAttribute("userRole", "normal");
            session.setAttribute("username", account);
            session.setAttribute("loggedIn", true);

            // Set cookies for session
            response.addCookie(createCookie("userRole", "normal", 3600));
            response.addCookie(createCookie("username", account, 3600));
            response.addCookie(createCookie("loggedIn", "true", 3600));

            out.print("{\"success\":true,\"message\":\"登录成功\",\"userRole\":\"normal\",\"username\":\"" + account + "\"}");
        } else {
            // Login failed
            out.print("{\"success\":false,\"message\":\"账号或密码错误\"}");
        }
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("application/json;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.print("{\"status\":\"ok\",\"message\":\"Login endpoint available\",\"methods\":[\"POST\"]}");
    }

    private jakarta.servlet.http.Cookie createCookie(String name, String value, int maxAge) {
        jakarta.servlet.http.Cookie cookie = new jakarta.servlet.http.Cookie(name, value);
        cookie.setPath("/");
        cookie.setMaxAge(maxAge);
        return cookie;
    }
}