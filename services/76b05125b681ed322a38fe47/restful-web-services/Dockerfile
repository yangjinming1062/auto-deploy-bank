# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application (skip tests for faster build)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/target/*.jar app.jar

# Also save a copy for the entrypoint script
RUN cp /app/app.jar /app/built.jar

# Create the entrypoint script
RUN printf '#!/bin/sh\ncp /app/built.jar /app/target.jar\nexec java -jar /app/app.jar\n' > /entrypoint.sh && chmod +x /entrypoint.sh

# Expose the application port
EXPOSE 8080

# Run via entrypoint to copy JAR to mounted volume at runtime
ENTRYPOINT ["/entrypoint.sh"]