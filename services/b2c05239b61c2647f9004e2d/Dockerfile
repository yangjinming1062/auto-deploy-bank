# Multi-stage build for Redisson
# Stage 1: Build the project
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy entire project
COPY . .

# Build the project - build redisson-all which depends on redisson
# Use --also-make to build dependencies
RUN mvn clean package -DskipTests -B -pl redisson-all --also-make

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/redisson-all/target/redisson-all-*.jar app.jar

# Copy configuration files
COPY --from=builder /app/redisson.yaml .
COPY --from=builder /app/redisson.json .

# Create non-root user
RUN addgroup -g 1001 -S redisson && \
    adduser -u 1001 -S redisson -G redisson && \
    chown -R redisson:redisson /app

USER redisson

# RedissonNode doesn't expose HTTP endpoints - it's a background service
# Port 40218 was reserved for future monitoring but never implemented

# Health check - verify Java process is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD pgrep -f 'java.*app.jar' || exit 1

# Run the application
CMD ["java", "-jar", "app.jar", "redisson.yaml"]