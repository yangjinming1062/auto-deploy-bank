# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the project (skip tests for faster build)
RUN mvn clean package -DskipTests -B -Dlucene.version=9.9.1

# Stage 2: Runtime image
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Set environment variables for Anserini
ENV ANSERINI_INDEX_CACHE=/root/.cache/pyserini/indexes
ENV JAVA_OPTS="-Xms512m -Xmx1g"

# Create cache directory
RUN mkdir -p /root/.cache/pyserini/indexes

# Copy the fatjar from builder stage to the required path for security scanning
COPY --from=builder /app/target/*-fatjar.jar /app/target.jar

# Create startup script
COPY <<'EOF' /start.sh
#!/bin/sh
echo "Starting Anserini Server..."
exec java $JAVA_OPTS -cp /app/target.jar io.anserini.server.AnseriniServer
EOF
RUN chmod +x /start.sh

# Expose the service port
EXPOSE 8080

# Run the application
CMD ["/start.sh"]