# Multi-stage build for Java/Spring Boot application

# Stage 1: Builder stage with Maven and JDK 17
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for better layer caching
COPY pom.xml .

# Download dependencies (this layer will be cached if pom.xml doesn't change)
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application (skip tests for faster build)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage with JRE only
FROM eclipse-temurin:17-jre-alpine

# Install wget for healthcheck
RUN apk add --no-cache wget

# Create app directory
WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/target/*.jar target.jar

# Expose port 8080
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "target.jar"]