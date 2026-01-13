# Multi-stage build for FastBee Spring Boot application

# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy main pom.xml first for better Docker layer caching
COPY springboot/pom.xml pom.xml

# Copy all modules to root level for Maven to find them
COPY springboot/fastbee-admin ./fastbee-admin
COPY springboot/fastbee-framework ./fastbee-framework
COPY springboot/fastbee-plugs ./fastbee-plugs
COPY springboot/fastbee-common ./fastbee-common
COPY springboot/fastbee-gateway ./fastbee-gateway
COPY springboot/fastbee-server ./fastbee-server
COPY springboot/fastbee-protocol ./fastbee-protocol
COPY springboot/fastbee-open-api ./fastbee-open-api
COPY springboot/fastbee-service ./fastbee-service

# Build the application (skip tests for production build)
RUN mvn clean package -DskipTests -B

# Stage 2: Create runtime image
FROM eclipse-temurin:17-jre-alpine

# Create app directory
WORKDIR /app

# Copy JAR from builder stage and rename to target.jar for volume mounting
COPY --from=builder /app/fastbee-admin/target/fastbee-admin.jar target.jar

# Also create app.jar (alias for running the application)
RUN ln -s target.jar app.jar

# Expose the required ports
EXPOSE 8080 1883 8083 5061

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/actuator/health || exit 1

# Run the application
CMD ["java", "-jar", "app.jar"]