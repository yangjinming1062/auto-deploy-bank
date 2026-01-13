##
## Multi-stage build for Lowcoder API Service
## Stage 1: Build with Maven
##
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy source code first
COPY server/api-service ./server/api-service

# Build the application and create assembly
# Build only lowcoder-server and its dependencies (excluding plugins)
RUN cd server/api-service && mvn clean package -DskipTests -B -DfailIfNoModules=false -pl lowcoder-server,lowcoder-domain,lowcoder-infra,lowcoder-sdk -am

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# Set working directory
WORKDIR /app

# Install curl for healthcheck
RUN apk add --no-cache curl

# Create app user (Alpine BusyBox compatible)
RUN addgroup -g 9001 lowcoder \
    && adduser -u 9001 -G lowcoder -s /bin/sh -D lowcoder

# Create necessary directories
RUN mkdir -p /app/target /app/libs /app/config /app/logs /app/plugins && \
    chown -R lowcoder:lowcoder /app

# Copy JAR from builder stage (extract from assembly)
COPY --from=builder /app/server/api-service/lowcoder-server/target/lowcoder-api-service-bin/lowcoder-api-service.jar /app/target.jar

# Copy dependencies (no plugins to copy since we skipped the plugins module)
COPY --from=builder /app/server/api-service/lowcoder-server/target/lowcoder-api-service-bin/libs/ /app/libs/

# Copy configuration
COPY server/api-service/lowcoder-server/src/main/resources/application.yaml /app/config/

# Switch to lowcoder user
USER lowcoder

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/api/status/health || exit 1

# Set environment variables
ENV JAVA_OPTS="-Xmx2G -Xms512M"
ENV APP_JAR="/app/target.jar"
ENV CLASSPATH="/app/target.jar:/app/libs/*"

# Run the application
CMD ["java", "-jar", "/app/target.jar"]