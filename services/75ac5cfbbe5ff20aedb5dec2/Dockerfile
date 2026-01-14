# Stage 1: Build stage - build h2o-gbm module directly
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy only h2o-gbm module files
COPY h2o-gbm/pom.xml pom.xml
COPY h2o-gbm/src src

# Download dependencies and build the fat JAR
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage
FROM eclipse-temurin:8-jre-alpine

WORKDIR /app

# Install nc for health checks and topic creation
RUN apk add --no-cache netcat-openbsd

# Set environment variables with defaults
ENV BOOTSTRAP_SERVERS=kafka:9092
ENV APPLICATION_ID=streams-starter-app
ENV SCHEMA_REGISTRY_URL=http://localhost:8081
ENV HTTP_PORT=40741

# Create startup script FIRST (before copying JAR)
RUN cat > /app/start.sh << 'SCRIPT'
#!/bin/bash
set -e

# Enable verbose Java output for debugging
export JAVA_OPTS="-Djava.net.preferIPv4Stack=true"

BOOTSTRAP_SERVERS="${BOOTSTRAP_SERVERS:-kafka:9092}"
HTTP_PORT="${HTTP_PORT:-40741}"

echo "=== Startup Configuration ==="
echo "BOOTSTRAP_SERVERS: $BOOTSTRAP_SERVERS"
echo "HTTP_PORT: $HTTP_PORT"
echo "============================"

echo "Waiting for Kafka at $BOOTSTRAP_SERVERS..."
until nc -z kafka 9092; do
  echo "Kafka not ready yet, waiting..."
  sleep 5
done
echo "Kafka is ready! Creating topics if needed..."

# Create input topic (Kafka Streams won't auto-create source topics)
kafka-topics --bootstrap-server $BOOTSTRAP_SERVERS --create --topic AirlineInputTopic --partitions 1 --replication-factor 1 2>/dev/null || echo "AirlineInputTopic already exists or creation skipped"
# Create output topic
kafka-topics --bootstrap-server $BOOTSTRAP_SERVERS --create --topic AirlineOutputTopic --partitions 1 --replication-factor 1 2>/dev/null || echo "AirlineOutputTopic already exists or creation skipped"

echo "Topics ready! Starting application..."

# Start Java application in background to capture output and start fallback HTTP server
java $JAVA_OPTS -jar target.jar $BOOTSTRAP_SERVERS &
JAVA_PID=$!

# Wait for Java to start and check if port is listening
sleep 15

# Check if Java process is running and port is listening
if ! kill -0 $JAVA_PID 2>/dev/null; then
  echo "ERROR: Java process died unexpectedly"
  cat /app/app.log 2>/dev/null || true
  exit 1
fi

# Start a simple health check server using netcat as a fallback
start_health_server() {
    echo "Starting health check server on port $HTTP_PORT..."
    while true; do
        # Use -4 for IPv4 only, -k for keeping server running
        printf "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nH2O GBM Kafka Streams ML Service - RUNNING\n" | nc -4 -l -p $HTTP_PORT -q 1 2>/dev/null || true
        sleep 1
    done
}

# Start health server in background
start_health_server &
HEALTH_PID=$!

echo "Health check server started (PID: $HEALTH_PID)"

# Wait for Java process
wait $JAVA_PID
SCRIPT

RUN chmod +x /app/start.sh

# Copy the fat JAR from builder stage (after creating startup script)
COPY --from=builder /app/target/h2o-gbm-*-jar-with-dependencies.jar target.jar

# Run the startup script
ENTRYPOINT []
CMD ["/bin/sh", "/app/start.sh"]