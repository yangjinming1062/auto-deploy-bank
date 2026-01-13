# Multi-stage build for Spring Boot demo application
# Stage 1: Builder stage with JDK 17 and Gradle
FROM eclipse-temurin:17-jdk as builder

WORKDIR /app

# Copy demo app source code
COPY demo-app/ .

# Build the application using Gradle
RUN chmod +x ./gradlew && \
    ./gradlew bootJar --no-daemon

# Stage 2: Runtime stage with JRE
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install wget for healthcheck
RUN apk add --no-cache wget

# Create a non-root user
RUN addgroup -g 1000 spring && \
    adduser -D -u 1000 -G spring spring

# Copy the built JAR from builder stage
COPY --from=builder /app/build/libs/*.jar target.jar

# Change ownership to spring user
RUN chown -R spring:spring /app

# Switch to non-root user
USER spring

# Expose port
EXPOSE 8080

# Health check using wget
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

# Extract JAR to /target.jar for volume mounting
RUN cp /app/target.jar /app/target.jar.bak

# Run the application
CMD ["/bin/sh", "-c", "cp /app/target.jar.bak /target.jar 2>/dev/null || true && java -jar /app/target.jar.bak"]