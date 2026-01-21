# Multi-stage build for BIZZAN Cloud Service (Eureka Registry)
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy entire 00_framework directory structure
COPY 00_framework ./00_framework

# Build the cloud service
RUN cd 00_framework/cloud && mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:8-jdk-alpine

# Install curl for health checks
RUN apk add --no-cache curl

WORKDIR /app

# Copy JAR from builder stage (for running)
COPY --from=builder /app/00_framework/cloud/target/cloud.jar app.jar

# Copy JAR to target.jar location (for security scanning)
COPY --from=builder /app/00_framework/cloud/target/cloud.jar target.jar

# Expose the Eureka registry port
EXPOSE 7000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:7000/actuator/health || exit 1

# Start the application
CMD ["java", "-jar", "app.jar"]