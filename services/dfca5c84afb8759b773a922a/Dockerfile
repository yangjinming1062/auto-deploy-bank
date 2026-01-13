# Multi-stage build for Camunda 8 Orchestration Cluster
# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /build

# Copy Maven wrapper and all source code
COPY . .

# Build the application
RUN ./mvnw clean package -DskipTests -DskipChecks -B -pl dist -am && \
    mv dist/target/camunda-zeebe-*.jar camunda-zeebe.jar

# Stage 2: Create runtime image
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Create a non-root user for security
RUN addgroup --gid 1001 camunda && \
    adduser -S -G camunda -u 1001 -h /app camunda

# Copy the built JAR from the builder stage
COPY --from=builder /build/camunda-zeebe.jar /app/camunda.jar

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/config && \
    chown -R camunda:camunda /app

# Switch to non-root user
USER camunda

# Expose ports
# 8080: HTTP API (Operate, Tasklist, Identity)
# 9600: Actuator/Management
# 26500: Zeebe Gateway
# 26501-26502: Zeebe internal ports
EXPOSE 8080 9600 26500 26501 26502

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:9600/actuator/health || exit 1

# Start the application
CMD ["java", "-jar", "camunda.jar"]