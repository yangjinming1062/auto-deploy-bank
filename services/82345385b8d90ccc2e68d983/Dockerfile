# Multi-stage build for jiron-gateway
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy entire project structure first
COPY . .

# Download dependencies (including all modules)
RUN mvn dependency:go-offline -B

# Build the gateway module (this will also build required dependencies)
RUN mvn clean package -DskipTests -B -pl jiron-gateway -am

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create target directory for volume mount (security scanning)
RUN mkdir -p /app/target

# Volume mount for JAR file extraction/security scanning
VOLUME /app/target

# Copy the built JAR from builder stage
COPY --from=builder /app/jiron-gateway/target/jiron-gateway.jar app.jar

# Expose the application port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]