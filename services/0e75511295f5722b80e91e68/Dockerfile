# Multi-stage build for Gradle project
# Stage 1: Build stage
FROM gradle:8.5-jdk17-alpine AS builder

WORKDIR /build

# Copy build configuration files first for better cache utilization
COPY build.gradle.kts settings.gradle.kts gradle.properties ./
COPY gradle ./gradle

# Copy source code
COPY src ./src
COPY src9 ./src9
COPY test-normal ./test-normal
COPY test-javaFx ./test-javaFx
COPY test-swt ./test-swt
COPY test-resources ./test-resources

# Build the project (compile + JAR creation)
RUN gradle clean normalShadowJar --no-daemon

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install Python for HTTP server
RUN apk add --no-cache python3

# Copy the built JAR from builder stage for security scanning
COPY --from=builder /build/build/libs/SystemTray-Example.jar target.jar

# Create a simple HTML info page
RUN echo '<!DOCTYPE html><html><head><title>SystemTray Library</title></head><body><h1>SystemTray Library</h1><p>This is a cross-platform System Tray library for Java.</p><p>Supported platforms: Linux (GtkStatusIcon, AppIndicator), macOS (AWT), Windows (Native, Swing).</p></body></html>' > index.html

# Expose the port
EXPOSE 8080

# Default command - run Python HTTP server
CMD ["python", "-m", "http.server", "8080"]