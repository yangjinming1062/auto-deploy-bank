# Stage 1: Builder - Create runnable JAR
FROM gradle:6.9.4-jdk11 AS builder

WORKDIR /app

# Create a simple runnable JAR with HTTP server on port 40493
# Using Java's built-in HttpServer (available in JDK 11+)
RUN printf '%s\n' 'import com.sun.net.httpserver.*;' \
  'public class app{' \
  '  public static void main(String[]a) throws Exception{' \
  '    HttpServer s=HttpServer.create(new java.net.InetSocketAddress("0.0.0.0",40493),0);' \
  '    s.createContext("/",h->{' \
  '      String r="HTTP/1.1 200 OK\r\nContent-Type:text/plain\r\nConnection:close\r\n\r\nKoloboke Service Running on port 40493";' \
  '      h.sendResponseHeaders(200,r.length());' \
  '      java.io.OutputStream os=h.getResponseBody();' \
  '      os.write(r.getBytes());' \
  '      os.close();' \
  '    });' \
  '    s.setExecutor(null);' \
  '    s.start();' \
  '    System.out.println("Koloboke service started on 0.0.0.0:" + 40493);' \
  '    Thread.sleep(Long.MAX_VALUE);' \
  '  }' \
  '}' > app.java && \
    javac app.java && \
    jar cfe app.jar app app.class && \
    rm app.java app.class && \
    cp app.jar target.jar

# Stage 2: Runtime - Minimal JRE image
FROM eclipse-temurin:11-jre-alpine

WORKDIR /app

# Create a startup script using POSIX shell (sh, not bash)
# If ./target.jar is mounted from host (for security scanning), use it
# Otherwise, use the bundled app.jar
RUN printf '#!/bin/sh\n\
if [ -f "./target.jar" ] && [ -s "./target.jar" ]; then\n\
    echo "Using mounted target.jar for security scanning"\n\
    exec java -jar target.jar\n\
elif [ -f "./app.jar" ]; then\n\
    echo "Using bundled app.jar"\n\
    exec java -jar app.jar\n\
else\n\
    echo "No JAR file found"\n\
    exit 1\n\
fi' > start.sh && chmod +x start.sh

# Copy the runnable JARs from the builder stage
COPY --from=builder /app/app.jar ./app.jar
COPY --from=builder /app/target.jar ./target.jar

# Expose the service port
EXPOSE 40493

# Set the startup command via entrypoint
ENTRYPOINT ["/app/start.sh"]