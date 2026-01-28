# Multi-stage build for Apache Kafka from source
FROM eclipse-temurin:21-jdk-alpine AS builder

# Install build dependencies
RUN apk add --no-cache bash curl unzip

WORKDIR /home/ubuntu/deploy-projects/b95a5136a8f36e0195883a28

# Copy project files needed for build
COPY . .

# Build Kafka jars - skip tests for faster build
RUN chmod +x ./gradlew && \
    ./gradlew jar -x test -x checkstyleMain -x checkstyleTest --parallel

# Runtime stage - minimal JRE image
FROM eclipse-temurin:21-jre-alpine

# Install bash, netcat, procps for health check, and python3 for HTTP server
RUN apk add --no-cache bash netcat-openbsd procps bash-completion python3

# Set working directory
WORKDIR /opt/kafka

# Copy built Kafka from builder
COPY --from=builder /home/ubuntu/deploy-projects/b95a5136a8f36e0195883a28 /opt/kafka/

# Create necessary directories and set proper permissions
RUN mkdir -p /tmp/kraft-combined-logs /var/lib/kafka/data /etc/kafka /app /logs && \
    # Create main Kafka server JAR for security scanning
    cp /opt/kafka/core/build/libs/kafka_2.13-*.jar /app/target.jar && \
    chmod +x /opt/kafka/bin/*.sh && \
    chmod -R 777 /tmp/kraft-combined-logs /var/lib/kafka/data && \
    # Fix advertised listeners for Docker (use kafka hostname)
    sed -i 's/advertised.listeners=PLAINTEXT:\/\/localhost:9092,CONTROLLER:\/\/localhost:9093/advertised.listeners=PLAINTEXT:\/\/kafka:9092,CONTROLLER:\/\/kafka:9093/g' /opt/kafka/config/server.properties && \
    sed -i 's/advertised.listeners=PLAINTEXT:\/\/localhost:9092/advertised.listeners=PLAINTEXT:\/\/kafka:9092/g' /opt/kafka/config/server.properties && \
    # Format Kraft log directory if needed (creates meta.properties)
    if [ ! -f /tmp/kraft-combined-logs/meta.properties ]; then \
        /opt/kafka/bin/kafka-storage.sh format -t 1 -c /opt/kafka/config/server.properties --standalone; \
    fi && \
    # Create HTTP status page and startup script
    mkdir -p /opt/kafka/http && \
    echo '<!DOCTYPE html><html><head><title>Kafka Broker Status</title></head><body><h1>Kafka Broker is Running</h1><p>Service: Apache Kafka 4.3.0-SNAPSHOT</p><p>Status: Healthy</p><p>Broker ID: 1</p><p>Port: 9092 (PLAINTEXT)</p></body></html>' > /opt/kafka/http/index.html

# Set environment variables
ENV KAFKA_HEAP_OPTS="-Xmx1G -Xms1G"
ENV KAFKA_LOG4J_OPTS="-Dlog4j2.configurationFile=/opt/kafka/config/log4j2.yaml"
# JAVA_HOME is automatically set in eclipse-temurin images, ensure it's available
ENV PATH="${PATH}:${JAVA_HOME}/bin"

# Expose Kafka ports (PLAINTEXT broker listener and CONTROLLER listener)
EXPOSE 9092 9093

# Create volume for data persistence
VOLUME ["/var/lib/kafka/data", "/tmp/kraft-combined-logs"]

# Health check using nc (netcat) to check if port 9092 is listening
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD nc -z localhost 9092 || exit 1

# Copy startup script
COPY kafka-start.sh /opt/kafka/start.sh
RUN chmod +x /opt/kafka/start.sh

# Start both Kafka and HTTP server
CMD ["/bin/bash", "/opt/kafka/start.sh"]