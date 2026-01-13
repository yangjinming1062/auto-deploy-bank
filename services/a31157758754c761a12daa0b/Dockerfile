# Multi-stage build for Java/Spring Boot application

# Stage 1: Builder stage with Maven and JDK 17
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy pom.xml from demo-service
COPY demo-service/pom.xml ./pom.xml

# Download dependencies (this layer will be cached if pom.xml doesn't change)
RUN mvn dependency:go-offline -B

# Copy source code from demo-service
COPY demo-service/src ./src

# Build the application (skip tests for faster build)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage with JRE only
FROM eclipse-temurin:17-jdk-alpine

# Install wget for healthcheck
RUN apk add --no-cache wget

# Create app directory
WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /build/target/*.jar target.jar

# Expose port 8080
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "target.jar"]