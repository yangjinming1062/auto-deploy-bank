# Multi-stage build for cloud service (Eureka Registry)
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml and download dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin-17-jre-alpine

# Install curl for health checks
RUN apk add --no-cache curl

WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/target/cloud.jar app.jar

# Expose the Eureka registry port
EXPOSE 7000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:7000/actuator/health || exit 1

# Start the application
CMD ["java", "-jar", "app.jar"]