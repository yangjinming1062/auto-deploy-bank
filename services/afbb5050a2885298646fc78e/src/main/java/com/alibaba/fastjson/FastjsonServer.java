package com.alibaba.fastjson;

import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;

public class FastjsonServer {
    public static void main(String[] args) throws Exception {
        int port = Integer.parseInt(System.getProperty("server.port", "8080"));

        Server server = new Server(port);
        ServletContextHandler context = new ServletContextHandler(ServletContextHandler.SESSIONS);
        context.setContextPath("/");
        server.setHandler(context);

        context.addServlet(new ServletHolder(new HttpServlet() {
            @Override
            protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
                resp.setContentType("application/json");
                PrintWriter writer = resp.getWriter();
                writer.write("{\"status\":\"ok\",\"message\":\"fastjson server running\"}");
            }

            @Override
            protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
                resp.setContentType("application/json");
                String json = req.getParameter("json");
                PrintWriter writer = resp.getWriter();
                try {
                    if (json != null && !json.isEmpty()) {
                        JSONObject obj = JSON.parseObject(json);
                        writer.write("{\"status\":\"ok\",\"parsed\":" + obj.toString() + "}");
                    } else {
                        writer.write("{\"status\":\"error\",\"message\":\"json parameter required\"}");
                    }
                } catch (Exception e) {
                    writer.write("{\"status\":\"error\",\"message\":\"" + e.getMessage() + "\"}");
                }
            }
        }), "/");

        context.addServlet(new ServletHolder(new HttpServlet() {
            @Override
            protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
                resp.setContentType("application/json");
                PrintWriter writer = resp.getWriter();
                writer.write("{\"status\":\"ok\",\"message\":\"fastjson server running\"}");
            }

            @Override
            protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
                resp.setContentType("application/json");
                String json = req.getParameter("json");
                PrintWriter writer = resp.getWriter();
                try {
                    if (json != null && !json.isEmpty()) {
                        JSONObject obj = JSON.parseObject(json);
                        writer.write("{\"status\":\"ok\",\"parsed\":" + obj.toString() + "}");
                    } else {
                        writer.write("{\"status\":\"error\",\"message\":\"json parameter required\"}");
                    }
                } catch (Exception e) {
                    writer.write("{\"status\":\"error\",\"message\":\"" + e.getMessage() + "\"}");
                }
            }
        }), "/api/parse");

        context.addServlet(new ServletHolder(new HttpServlet() {
            @Override
            protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
                resp.setContentType("text/plain");
                PrintWriter writer = resp.getWriter();
                writer.write("Fastjson Library Running");
            }
        }), "/version");

        System.out.println("Starting Fastjson server on port " + port + "...");
        server.start();
        System.out.println("Fastjson server started at http://localhost:" + port);
        server.join();
    }
}