# Multi-stage build for Spring Boot application with Gradle

# Stage 1: Builder
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /app

# Copy gradle wrapper and build files first for better caching
COPY gradlew ./
COPY gradle ./gradle
COPY build.gradle.kts ./
COPY settings.gradle.kts ./

# Copy source code
COPY src ./src

# Make gradlew executable
RUN chmod +x gradlew

# Generate JOOQ code first (required for compilation)
RUN ./gradlew jooqCodegen --no-daemon

# Build the application
RUN ./gradlew bootJar -x test --no-daemon

# Stage 2: Runtime
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Create non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy the built JAR from builder stage
COPY --from=builder /app/build/libs/backend.jar target.jar

# Create log directory
RUN mkdir -p /var/log && chown -R appuser:appgroup /var/log

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

# Run the application
CMD ["java", "-jar", "target.jar"]