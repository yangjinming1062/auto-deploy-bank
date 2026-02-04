# Stage 1: Builder - Build the application with Gradle
FROM gradle:8.5-jdk17-alpine AS builder

WORKDIR /app

# Copy build configuration files first for better caching
COPY build.gradle.kts settings.gradle.kts gradle.properties ./
COPY gradle ./gradle

# Copy source code
COPY src ./src

# Build the application (skip tests, create shadow/fat JAR)
RUN gradle build -x test --no-daemon

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install required tools for healthcheck
RUN apk add --no-cache wget curl netcat-openbsd

# Create non-root user for security
RUN addgroup -S app && adduser -S -G app app

# Copy the built JAR from builder stage
# The Shadow plugin creates a fat JAR in build/libs/
COPY --from=builder /app/build/libs/*.jar target.jar

# Copy config directory
COPY config ./config

# Change ownership to non-root user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose the application port
EXPOSE 8081

# Health check - check if Java process is running and port is listening
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD pgrep -f "java.*target.jar" && (nc -z 127.0.0.1 8081 || exit 1) || exit 1

# Run the application with config file argument
ENTRYPOINT ["sh", "-c"]
CMD ["java -jar /app/target.jar /app/config/config.json5"]

# Environment variables
ENV SERVER_PORT=8081