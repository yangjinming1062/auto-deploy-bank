# Multi-stage build for Genie Application
# Stage 1: Runtime image with JRE
FROM eclipse-temurin:17-jre-alpine

# Install minimal runtime dependencies
RUN apk add --no-cache procps curl bash

# Create non-root user for security
RUN addgroup -S genie && adduser -S genie -G genie

# Create required directories for Genie with proper permissions
RUN mkdir -p /tmp/genie/attachments /tmp/genie/archives /tmp/genie/jobs && \
    chown -R genie:genie /tmp/genie

WORKDIR /app

# Copy application JAR (must be built first with: ./gradlew bootJar -p genie-app --no-daemon -x test)
# The JAR file should be placed at: genie-app/build/libs/genie-app-*.jar
COPY genie-app/build/libs/genie-app-*.jar target.jar

# Copy agent JAR (must be built first with: ./gradlew bootJar -p genie-agent-app --no-daemon -x test)
COPY genie-agent-app/build/libs/genie-agent-app-*.jar genie-agent.jar

# Change ownership to non-root user
RUN chown -R genie:genie /app

# Switch to non-root user
USER genie

# Expose HTTP and gRPC ports
EXPOSE 8080 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/admin/health || exit 1

# Run the application
ENTRYPOINT ["java", \
            "-Djava.security.egd=file:/dev/./urandom", \
            "-Dgenie.agent.launcher.local.agent-jar-path=/app/genie-agent.jar", \
            "-Dgenie.jobs.agent-execution.agent-probability=1.0", \
            "-jar", \
            "/app/target.jar" \
            ]