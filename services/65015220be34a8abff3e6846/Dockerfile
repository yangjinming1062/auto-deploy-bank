# Multi-stage build for Spring Boot application
# Stage 1: Builder stage with Maven and JDK
FROM maven:3-eclipse-temurin-8 AS builder

# Set working directory
WORKDIR /app

# Copy minimal parent pom.xml (only with mall-tiny module) and mall-tiny
COPY temp-pom.xml ./pom.xml
COPY mall-tiny/ ./mall-tiny/

# Build the mall-tiny module with Lombok annotation processing
RUN mvn clean package -DskipTests -B -pl mall-tiny

# Stage 2: Runtime stage with JRE only
FROM eclipse-temurin:8-jre-alpine

# Install curl for healthchecks
RUN apk --no-cache add curl

# Set working directory
WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/mall-tiny/target/*.jar app.jar
COPY --from=builder /app/mall-tiny/target/*.jar /scan/app.jar

# Create app directories
RUN mkdir -p /app/logs /scan

# Create entrypoint script for JAR extraction
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'cp /scan/app.jar /target.jar' >> /entrypoint.sh && \
    echo 'exec java -jar /app/app.jar "$@"' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/actuator/health || exit 1

# Use entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
CMD []