# Multi-stage build for Google Cloud Demo Service
# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml and download dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Create runtime image
FROM alpine:latest

# Install Java
RUN apk add --no-cache openjdk17-jre

# Create app directory
WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/target/*.jar target.jar

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/api/translate/health || exit 1

# Run the application
CMD ["java", "-jar", "target.jar"]