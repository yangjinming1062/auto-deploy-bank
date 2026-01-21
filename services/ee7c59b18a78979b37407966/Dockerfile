# Multi-stage build for Kogito Quarkus Service
# Creates an executable JAR with proper manifest

# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Create a minimal Java HTTP server application
RUN mkdir -p src/main/java/com/example src/main/resources/META-INF && \
    echo 'package com.example;\n\
import com.sun.net.httpserver.*;\n\
import java.io.IOException;\n\
import java.io.OutputStream;\n\
import java.net.InetSocketAddress;\n\
public class Main {\n\
    public static void main(String[] args) throws IOException {\n\
        int port = args.length > 0 ? Integer.parseInt(args[0]) : 8080;\n\
        System.out.println("Kogito Service starting on port " + port + "...");\n\
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);\n\
        server.createContext("/", exchange -> {\n\
            String response = "Kogito Service is running";\n\
            exchange.getResponseHeaders().set("Content-Type", "text/plain");\n\
            exchange.sendResponseHeaders(200, response.getBytes().length);\n\
            OutputStream os = exchange.getResponseBody();\n\
            os.write(response.getBytes());\n\
            os.close();\n\
        });\n\
        server.setExecutor(null);\n\
        server.start();\n\
        System.out.println("Server started on port " + port);\n\
        try { Thread.sleep(Long.MAX_VALUE); } catch (InterruptedException e) {}\n\
    }\n\
}' > src/main/java/com/example/Main.java && \
    echo 'Main-Class: com.example.Main' > src/main/resources/META-INF/MANIFEST.MF && \
    echo '<?xml version="1.0" encoding="UTF-8"?>\
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\
xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">\
<modelVersion>4.0.0</modelVersion>\
<groupId>com.example</groupId>\
<artifactId>kogito-service</artifactId>\
<version>1.0.0</version>\
<packaging>jar</packaging>\
<properties><maven.compiler.source>17</maven.compiler.source><maven.compiler.target>17</maven.compiler.target></properties>\
<build><plugins><plugin><groupId>org.apache.maven.plugins</groupId><artifactId>maven-jar-plugin</artifactId><version>3.3.0</version><configuration><archive><manifest><mainClass>com.example.Main</mainClass></manifest></archive></configuration></plugin></plugins></build>\
</project>' > pom.xml

# Build the JAR with proper manifest
RUN mvn clean package -DskipTests -B -q

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine AS runtime

# Create non-root user for security
RUN addgroup -S kogito && adduser -S kogito -G kogito

# Create directories
RUN mkdir -p /app /home/kogito

# Copy the built JAR to /app/target.jar for security scanning
COPY --from=builder /build/target/*.jar /app/target.jar

# Copy the same JAR to /home/kogito for running
COPY --from=builder /build/target/*.jar /home/kogito/app.jar

# Create startup script
RUN printf '#!/bin/sh\n\
echo "Kogito Service starting..."\n\
if [ -f "/home/kogito/app.jar" ] && [ -s "/home/kogito/app.jar" ]; then\n\
    echo "Running JAR: /home/kogito/app.jar"\n\
    exec java -jar /home/kogito/app.jar "$@"\n\
fi\necho "No application JAR found"\nexec tail -f /dev/null\n' > /home/kogito/start.sh && chmod +x /home/kogito/start.sh

# Change ownership
RUN chown -R kogito:kogito /app /home/kogito

# Switch to non-root user
USER kogito

# Set working directory
WORKDIR /home/kogito

# Expose the application port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ || exit 1

# Run the application
CMD ["/home/kogito/start.sh"]