# Multi-stage build for Spring Boot application
# Stage 1: Builder stage using Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy root pom.xml first
COPY pom.xml .

# Copy all module directories at the correct relative paths
COPY channels ./channels
COPY modules ./modules
COPY plugins ./plugins
COPY starter ./starter

# Build the application (skip tests for production build)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage using JRE
FROM eclipse-temurin:17-jre-alpine

# Maintainer label
LABEL maintainer="270580156@qq.com"

# Set working directory
WORKDIR /app

# Copy the built JAR from builder stage
# The JAR file will be copied and renamed to app.jar
COPY --from=builder /app/starter/target/bytedesk-starter.jar app.jar

# Also copy as target.jar for security scanning (mounted volume will override)
COPY --from=builder /app/starter/target/bytedesk-starter.jar target.jar

# Create uploads directory
RUN mkdir -p /app/uploads

# Expose the application port
EXPOSE 9003

# Set JVM options for better container performance
ENV JAVA_OPTS="-Xms512m -Xmx1024m -XX:+UseG1GC"

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]