# Multi-stage build for Apache Geode Pulse (Web UI)
# Stage 1: Prepare Jetty Runner
FROM eclipse-temurin:8-jdk as builder

WORKDIR /tmp

# Download Jetty Runner for running the WAR file
RUN wget -q https://repo1.maven.org/maven2/org/eclipse/jetty/jetty-runner/9.4.48.v20220622/jetty-runner-9.4.48.v20220622.jar -O jetty-runner.jar

# Stage 2: Runtime image with geode-pulse web UI
FROM eclipse-temurin:8-jdk-alpine

WORKDIR /app

# Install curl for health checks
RUN apk add --no-cache curl

# Copy Jetty Runner from builder stage
COPY --from=builder /tmp/jetty-runner.jar /app/jetty-runner.jar

# Copy the pre-built geode-pulse WAR file
COPY target.jar /app/app.war

# Copy entrypoint script to handle pulse-users.properties override
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV JAVA_OPTS="-Xmx512m -Xms256m"

# Expose port 8080 (will be mapped to 40291)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/ || exit 1

# Start the geode-pulse web UI
ENTRYPOINT ["/app/entrypoint.sh"]

# Add volume mount for security scanning
VOLUME ["/app/target.jar"]