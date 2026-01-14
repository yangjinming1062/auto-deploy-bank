# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy entire source code (including pom.xml and all module directories)
COPY . .

# Build the project (multi-module Maven project)
# This will download all dependencies and build all modules
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# Install required packages
RUN apk add --no-cache curl tzdata fontconfig ttf-dejavu

# Set timezone
ENV TZ=Asia/Shanghai

WORKDIR /application

# Copy the built JAR from builder stage
COPY --from=builder /app/tduck-api/target/tduck-api.jar app.jar

# Create upload directory for file uploads
RUN mkdir -p /application/BOOT-INF/lib/upload

# Create scan directory for security scanning
RUN mkdir -p /scan

# Copy JAR to scan directory for security scanning
RUN cp /application/app.jar /scan/target.jar

# Expose application port
EXPOSE 8999

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -sf http://localhost:8999/v3/api-docs && echo 'OK'

# Run Spring Boot application
ENTRYPOINT ["java", "-jar", "/application/app.jar"]