# Multi-stage build for Ktor application

# Build stage
FROM gradle:8.11-jdk17 AS builder

WORKDIR /app

# Copy Gradle configuration files
COPY build.gradle.kts .
COPY settings.gradle.kts .
COPY gradle.properties .
COPY gradlew .
COPY postgres.yaml .

# Make gradlew executable
RUN chmod +x gradlew

# Copy gradle wrapper directory
COPY gradle/ ./gradle/

# Copy source code
COPY src/ ./src/

# Build the application
RUN ./gradlew build --no-daemon

# Runtime stage
FROM eclipse-temurin:24-jre-alpine

# Install curl for healthcheck
RUN apk --no-cache add curl

WORKDIR /app

# Copy built JAR from builder stage
COPY --from=builder /app/build/libs/*.jar /app/app.jar

# Copy postgres.yaml configuration and modify it for docker
COPY --from=builder /app/postgres.yaml /app/postgres.yaml

# Create entrypoint script to start the application on port 40962
RUN echo '#!/bin/sh' > /app/start.sh && \
    echo 'exec java -Dktor.deployment.port=40962 -jar /app/app.jar "$@"' >> /app/start.sh && \
    chmod +x /app/start.sh

# Expose the internal port (Ktor default)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Run the application using Netty engine
ENTRYPOINT ["/app/start.sh"]