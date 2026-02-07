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
 * Logout servlet for session cleanup
 */
@WebServlet(urlPatterns = {"/public/logout.do", "/logout"})
public class LogoutServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("application/json;charset=UTF-8");
        PrintWriter out = response.getWriter();

        // Invalidate session
        HttpSession session = request.getSession(false);
        if (session != null) {
            session.invalidate();
        }

        // Clear cookies
        response.addCookie(createCookie("userRole", "", 0));
        response.addCookie(createCookie("username", "", 0));
        response.addCookie(createCookie("loggedIn", "", 0));

        out.print("{\"success\":true,\"message\":\"已退出登录\"}");
    }

    private jakarta.servlet.http.Cookie createCookie(String name, String value, int maxAge) {
        jakarta.servlet.http.Cookie cookie = new jakarta.servlet.http.Cookie(name, value);
        cookie.setPath("/");
        cookie.setMaxAge(maxAge);
        return cookie;
    }
}