# Multi-stage build for Spring Boot application
# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy all source code at once
COPY . .

# Build all dependencies first
RUN mvn clean install -DskipTests -B \
    -pl y9-digitalbase-common,y9-digitalbase-starter,y9-digitalbase-support,y9-digitalbase-idcode \
    -am

# Build the platform module with all dependencies
RUN mvn clean package -DskipTests -B \
    -pl y9-digitalbase-module/y9-module-platform/risenet-y9boot-server-platform \
    -am

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Set working directory
WORKDIR /app

# Copy JAR from builder stage and rename to app.jar
COPY --from=builder /app/y9-digitalbase-module/y9-module-platform/risenet-y9boot-server-platform/target/risenet-y9boot-server-platform-*.jar app.jar

# Also copy to target.jar location for security scanning volume mount
RUN cp app.jar target.jar

# Expose port 8080
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/server-platform/actuator/health || exit 1

# Run the application
CMD ["java", "-jar", "app.jar"]