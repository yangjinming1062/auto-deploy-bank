# Multi-stage build for KnowStreaming
# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy source code
COPY . .

# Build the application
RUN mvn -Prelease-package -Dmaven.test.skip=true clean install -U

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/km-rest/target/ks-km.jar target.jar

# Copy initialization script
COPY --from=builder /app/bin/init_es_template.sh /app/init_es_template.sh

# Make script executable
RUN chmod +x /app/init_es_template.sh

# Expose the application port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "target.jar"]