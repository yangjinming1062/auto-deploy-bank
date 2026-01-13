# Multi-stage build for Java Spring Boot application

# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy pom.xml and download dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage
FROM eclipse-temurin:8-jre-alpine

WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/target/java-sec-code-1.0.0.jar target.jar

# Expose port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "target.jar"]