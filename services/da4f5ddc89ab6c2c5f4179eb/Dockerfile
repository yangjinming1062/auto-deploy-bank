# Multi-stage build for Spring Boot application

# Stage 1: Build stage - Using pre-built JAR
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy the pre-built JAR
COPY target.jar .

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the JAR from builder stage
COPY --from=builder /app/target.jar app.jar

# Expose port 8080
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]