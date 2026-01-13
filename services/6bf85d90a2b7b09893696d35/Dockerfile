# Multi-stage build for LTS-Admin WAR application
# Stage 1: Build stage using Maven with Java 17
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy all source code
COPY . /build/

# Build only required dependencies for lts-admin (skip problematic modules)
RUN mvn clean install -U -DskipTests -B -q -pl lts-core,lts-monitor -am

# Build the WAR file
WORKDIR /build/lts-admin
RUN mvn clean package -DskipTests -B -q && \
    mv target/*.war app.war

# Stage 2: Runtime stage with JRE and Jetty
FROM jetty:9.4-jdk17-slim

WORKDIR /app

# Install wget for health checks
USER root
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*
USER jetty

# Copy the WAR file from builder stage
COPY --from=builder /build/lts-admin/app.war /var/lib/jetty/webapps/ROOT.war

# Extract the WAR file into ROOT directory
RUN cd /var/lib/jetty/webapps && \
    mkdir -p ROOT && \
    cd ROOT && \
    jar -xf ../ROOT.war && \
    cd .. && \
    rm ROOT.war

# Copy configuration files
COPY conf/ /app/conf/

# Create necessary directories
RUN mkdir -p /app/logs

# Create Jetty configuration to set port
RUN mkdir -p /var/lib/jetty/start.d && \
    echo "jetty.http.port=8081" > /var/lib/jetty/start.d/http-config.ini

# Create startup script
RUN echo '#!/bin/bash\n\
# Start Jetty\n\
cd /var/lib/jetty\n\
exec java $JAVA_OPTIONS -jar /usr/local/jetty/start.jar' > /app/start.sh && \
    chmod +x /app/start.sh

# Expose the port the app runs on
EXPOSE 8081

# Set JVM options (add --add-opens for Java 17 compatibility with Javassist)
ENV JAVA_OPTIONS="-Xms256m -Xmx512m -XX:+UseG1GC --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED"

# Use custom startup
CMD ["/app/start.sh"]
