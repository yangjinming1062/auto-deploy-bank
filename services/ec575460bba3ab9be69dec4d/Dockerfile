# Stage 1: Build with Gradle (using Gradle 6.9 for compatibility with older build.gradle)
FROM gradle:6.9.4-jdk11-alpine AS builder

WORKDIR /app

# Copy build configuration files first for better layer caching
COPY build.gradle settings.gradle gradle.properties ./
COPY examples/web-service/build.gradle ./examples/web-service/build.gradle

# Copy source code
COPY . .

# Build the project (skip tests for faster builds)
RUN gradle :examples:web-service:shadowJar --no-daemon

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/build/web-service/libs/*.jar app.jar

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the service port
EXPOSE 40695

# Run the application via entrypoint to copy JAR for scanning
ENTRYPOINT ["/entrypoint.sh"]