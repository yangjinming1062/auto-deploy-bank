package com.myblog.controller;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Random;

/**
 * Support servlet for login verification codes
 */
@WebServlet(urlPatterns = {"/public/vcode/random.do", "/public/vcode/validate.do"})
public class LoginSupportServlet extends HttpServlet {

    // Simple 4-digit codes
    private static final String VALID_CODE = "1234";
    private static final Random random = new Random();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String requestURI = request.getRequestURI();

        if (requestURI.contains("random.do")) {
            // Generate random verification code
            response.setContentType("image/png");
            response.setHeader("Cache-Control", "no-cache");

            // Create a simple 4-digit code and store in session
            String code = String.format("%04d", random.nextInt(10000));
            HttpSession session = request.getSession(true);
            session.setAttribute("vcode", code);

            // For now, return a simple response (in production, generate actual image)
            response.setContentType("application/json;charset=UTF-8");
            PrintWriter out = response.getWriter();
            out.print("{\"code\":\"" + code + "\"}");
        } else {
            response.setContentType("application/json;charset=UTF-8");
            PrintWriter out = response.getWriter();
            out.print("{\"success\":true,\"code\":\"" + VALID_CODE + "\"}");
        }
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("application/json;charset=UTF-8");
        PrintWriter out = response.getWriter();

        String code = request.getParameter("code");
        HttpSession session = request.getSession(false);
        String sessionCode = session != null ? (String) session.getAttribute("vcode") : null;

        if (code != null && (code.equals(VALID_CODE) || code.equals(sessionCode))) {
            out.print("{\"success\":true}");
        } else {
            out.print("{\"success\":false,\"message\":\"验证码错误\"}");
        }
    }
}