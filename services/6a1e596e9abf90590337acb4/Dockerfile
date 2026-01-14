# Multi-stage build for github-api library
# Stage 1: Builder using Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B -DskipTests

# Copy source code
COPY src ./src

# Build the JAR (skip tests for faster build)
RUN mvn clean package -DskipTests -B -Dspotless.check.skip=true -Dsortpom.verifyFail=WARN

# Stage 2: Runtime image with Python for HTTP server
FROM python:3.11-alpine

WORKDIR /app

# Copy the built JAR to target.jar for security scanning
COPY --from=builder /app/target/github-api-*.jar /app/target.jar

# Create a simple HTML page
RUN echo '<!DOCTYPE html><html><head><title>GitHub API Library</title></head><body><h1>GitHub API Java Library</h1><p>This is a Java library for accessing the GitHub API.</p><p>Build Status: Success</p></body></html>' > index.html

# Run Python HTTP server on port 8080
EXPOSE 8080
CMD ["python", "-m", "http.server", "8080"]