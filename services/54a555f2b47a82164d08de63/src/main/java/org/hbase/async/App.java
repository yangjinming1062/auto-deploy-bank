/*
 * AsyncHBase Service Application
 * A simple HTTP service that uses AsyncHBase client library
 */
package org.hbase.async;

import com.sun.net.httpserver.HttpServer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class App {
    private static final Logger LOG = LoggerFactory.getLogger(App.class);
    private static final int PORT = 44142;

    public static void main(String[] args) {
        LOG.info("Starting AsyncHBase Service on port {}", PORT);

        try {
            // Create HTTP server
            HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);

            // Health check endpoint
            server.createContext("/health", exchange -> {
                String response = "{\"status\":\"UP\",\"service\":\"asynchbase\"}";
                exchange.sendResponseHeaders(200, response.length());
                OutputStream os = exchange.getResponseBody();
                os.write(response.getBytes());
                os.close();
            });

            // Root endpoint
            server.createContext("/", exchange -> {
                String response = "AsyncHBase Service is running. " +
                    "Endpoints: /health, /status";
                exchange.sendResponseHeaders(200, response.length());
                OutputStream os = exchange.getResponseBody();
                os.write(response.getBytes());
                os.close();
            });

            // Status endpoint - shows HBase connection status
            server.createContext("/status", exchange -> {
                String status;
                int httpStatus = 200;

                try {
                    // Create HBase client with config from environment or defaults
                    // HBaseClient constructor takes quorum_spec and base_path directly
                    String zkQuorum = System.getProperty("hbase.zookeeper.quorum",
                        System.getenv().getOrDefault("HBASE_ZOOKEEPER_QUORUM", "localhost"));
                    String zkParent = System.getProperty("hbase.zookeeper.znode.parent",
                        System.getenv().getOrDefault("HBASE_ZOOKEEPER_ZNODE_PARENT", "/hbase"));

                    HBaseClient client = new HBaseClient(zkQuorum, zkParent);

                    status = String.format(
                        "{\"status\":\"UP\",\"hbase\":\"connected\",\"zookeeper\":\"%s\",\"parent\":\"%s\"}",
                        zkQuorum, zkParent
                    );

                    // Quick shutdown to verify connection
                    client.shutdown().joinUninterruptibly();
                } catch (Exception e) {
                    LOG.error("HBase connection error", e);
                    status = String.format(
                        "{\"status\":\"DOWN\",\"error\":\"%s\"}",
                        e.getMessage().replace("\"", "\\\"")
                    );
                    httpStatus = 503;
                }

                exchange.sendResponseHeaders(httpStatus, status.length());
                OutputStream os = exchange.getResponseBody();
                os.write(status.getBytes());
                os.close();
            });

            server.setExecutor(null);
            server.start();
            LOG.info("Server started on port {}", PORT);

            // Add shutdown hook
            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                LOG.info("Shutting down server...");
                server.stop(0);
            }));

        } catch (IOException e) {
            LOG.error("Failed to start server", e);
            System.exit(1);
        }
    }
}