# Multi-stage build for Ktor kweet sample application with PostgreSQL

# Build stage
FROM gradle:8.11-jdk17 AS builder

WORKDIR /app

# Copy Gradle configuration files
COPY kweet/build.gradle.kts .
COPY kweet/gradle.properties .
COPY kweet/gradlew .
COPY kweet/src/main/resources/application.conf .

# Make gradlew executable
RUN chmod +x gradlew

# Copy gradle wrapper directory
COPY kweet/gradle/ ./gradle/

# Copy source code
COPY kweet/src/ ./src/

# Build the application and create distribution
RUN ./gradlew distZip --no-daemon

# Runtime stage
FROM eclipse-temurin:17-jre-alpine

# Install curl and unzip for healthcheck and extraction
RUN apk --no-cache add curl unzip

WORKDIR /app

# Copy and extract the distribution
COPY --from=builder /app/build/distributions/app.zip ./
RUN unzip -q app.zip && rm app.zip && chmod +x app/bin/*

# Copy the main JAR for volume mount and security scanning
COPY --from=builder /app/build/libs/app.jar /app/original.jar

# Copy application configuration
COPY --from=builder /app/src/main/resources/ /app/build/distributions/app/resources/

# Create entrypoint script to start the application
# Configure using environment variables with sensible defaults
RUN echo '#!/bin/sh' > /app/start.sh && \
    echo 'PORT="${PORT:-8080}"' >> /app/start.sh && \
    echo 'HOST="${HOST:-0.0.0.0}"' >> /app/start.sh && \
    echo 'JDBC_URL="${JDBC_URL:-jdbc:postgresql://db:5432/articles}"' >> /app/start.sh && \
    echo 'JDBC_USER="${JDBC_USER:-user}"' >> /app/start.sh && \
    echo 'JDBC_PASSWORD="${JDBC_PASSWORD:-password}"' >> /app/start.sh && \
    echo 'mkdir -p /app/build' >> /app/start.sh && \
    echo 'cp /app/original.jar /app/target.jar' >> /app/start.sh && \
    echo 'export HOME=/app' >> /app/start.sh && \
    echo 'export JDBC_URL' >> /app/start.sh && \
    echo 'export JDBC_USER' >> /app/start.sh && \
    echo 'export JDBC_PASSWORD' >> /app/start.sh && \
    echo 'exec /app/app/bin/app -Dktor.deployment.port=$PORT -Dktor.deployment.host=$HOST "$@"' >> /app/start.sh && \
    chmod +x /app/start.sh

# Expose the internal port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Run the application
ENTRYPOINT ["/app/start.sh"]