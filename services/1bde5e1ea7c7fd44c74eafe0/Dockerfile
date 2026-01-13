# Multi-stage build for Smart Cloud Demo Application

# Stage 1: Builder stage with Maven and JDK 17
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy parent pom.xml first to leverage Docker cache
COPY pom.xml .

# Copy all smart cloud modules (needed for Maven validation)
COPY smart-api-core ./smart-api-core
COPY smart-cloud-starter ./smart-cloud-starter
COPY smart-cloud-demo ./smart-cloud-demo
COPY smart-code-generate ./smart-code-generate
COPY smart-common-pojo ./smart-common-pojo
COPY smart-common-web ./smart-common-web
COPY smart-constants ./smart-constants
COPY smart-exception ./smart-exception
COPY smart-mask ./smart-mask
COPY smart-test ./smart-test
COPY smart-utility ./smart-utility

# Download dependencies
RUN mvn dependency:go-offline -B

# Build the demo application
RUN mvn clean package -DskipTests -B -pl smart-cloud-demo

# Stage 2: Runtime stage with JRE 17
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install curl for health checks
RUN apk add --no-cache curl

# Copy the built JAR from builder stage
COPY --from=builder /app/smart-cloud-demo/target/*.jar app.jar

# Also copy to target.jar path for security scanning volume mount
RUN cp app.jar target.jar

# Expose the internal port (8080)
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]