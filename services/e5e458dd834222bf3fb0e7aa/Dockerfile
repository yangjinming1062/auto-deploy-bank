# Multi-stage build for Spring Initializr service

# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy entire project structure
COPY . .

# Build only the service-sample module from root with dependencies
RUN mvn clean package -DskipTests -B -pl initializr-service-sample -am

# Stage 2: Create runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /build/initializr-service-sample/target/initializr-service-sample-*.jar app.jar

# Create scans directory and copy JAR for security scanning
RUN mkdir -p /scans && cp app.jar /scans/target.jar

# Expose port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]