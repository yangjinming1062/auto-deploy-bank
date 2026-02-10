# Multi-stage Dockerfile for Quarkus application
# Stage 1: Build stage with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application (skip tests for production build)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine AS runtime

WORKDIR /app

# Expose the HTTP port
EXPOSE 8080

# Set the startup command - JAR comes from volume mount at /app/target.jar
CMD ["java", "-jar", "target.jar"]