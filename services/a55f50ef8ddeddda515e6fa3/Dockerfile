# Multi-stage build for Spring Boot application with Gradle
# Stage 1: Build the application
FROM gradle:7.4.2-jdk11 AS builder

WORKDIR /build

# Copy build configuration files
COPY build.gradle settings.gradle gradle.properties sonar-project.properties checkstyle.xml package.json package-lock.json angular.json tsconfig.json tsconfig.app.json tsconfig.spec.json ./
COPY gradle ./gradle
COPY webpack ./webpack

# Copy source code
COPY src ./src

# Build the application (skip tests and integration tests)
RUN gradle bootJar -x test -x integrationTest --no-daemon

# Stage 2: Runtime image
FROM eclipse-temurin:11-jdk-alpine

WORKDIR /app

# Install curl for healthcheck
RUN apk add --no-cache curl

# Copy the built JAR from builder stage
COPY --from=builder /build/build/libs/*.jar /app/target.jar

# Create scan directory
RUN mkdir -p /scan

# Expose the application port
EXPOSE 8080

# Run the application - copy JAR to scan path for security scanning
CMD sh -c "cp /app/target.jar /scan/target.jar && java -jar /app/target.jar"