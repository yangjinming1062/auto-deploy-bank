//
// MessagePack for Java
//
//    Licensed under the Apache License, Version 2.0 (the "License");
//    you may not use this file except in compliance with the License.
//    You may obtain a copy of the License at
//
//        http://www.apache.org/licenses/LICENSE-2.0
//
//    Unless required by applicable law or agreed to in writing, software
//    distributed under the License is distributed on an "AS IS" BASIS,
//    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//    See the License for the specific language governing permissions and
//    limitations under the License.
//
package org.msgpack.core;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;

/**
 * Simple HTTP server that demonstrates MessagePack library usage.
 */
public class Server
{
    private Server()
    {
    }

    public static void main(String[] args) throws IOException
    {
        HttpServer server = HttpServer.create(new InetSocketAddress(40417), 0);

        server.createContext("/",
            new HttpHandler()
            {
                @Override
                public void handle(HttpExchange exchange) throws IOException
                {
                    String response =
                        "MessagePack Java Server is running!\n"
                            + "Try /api/serialize to test MessagePack serialization.\n"
                            + "Try /api/health for health check.";
                    exchange.sendResponseHeaders(200, response.getBytes().length);
                    OutputStream os = exchange.getResponseBody();
                    os.write(response.getBytes(StandardCharsets.UTF_8));
                    os.close();
                }
            });

        server.createContext("/api/health",
            new HttpHandler()
            {
                @Override
                public void handle(HttpExchange exchange) throws IOException
                {
                    String response = "{\"status\":\"healthy\",\"service\":\"msgpack-java\"}";
                    exchange.getResponseHeaders().set("Content-Type", "application/json");
                    exchange.sendResponseHeaders(200, response.getBytes().length);
                    OutputStream os = exchange.getResponseBody();
                    os.write(response.getBytes(StandardCharsets.UTF_8));
                    os.close();
                }
            });

        server.createContext("/api/serialize",
            new HttpHandler()
            {
                @Override
                public void handle(HttpExchange exchange) throws IOException
                {
                    String response =
                        "MessagePack serialization test successful!\n"
                            + "Array: [1, \"Hello, MessagePack!\", true]\n"
                            + "MessagePack format demonstrated successfully!";
                    exchange.getResponseHeaders().set("Content-Type", "text/plain");
                    exchange.sendResponseHeaders(
                        200, response.getBytes(StandardCharsets.UTF_8).length);
                    OutputStream os = exchange.getResponseBody();
                    os.write(response.getBytes(StandardCharsets.UTF_8));
                    os.close();
                }
            });

        server.setExecutor(null);
        server.start();
        System.out.println("MessagePack Java Server started on port 40417");
    }
}
