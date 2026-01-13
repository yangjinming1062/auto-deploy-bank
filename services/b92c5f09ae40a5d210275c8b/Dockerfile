#############################################################
# Multi-stage Dockerfile to build INCEpTION container image
#############################################################

# Stage 1: Build stage with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy the entire project
COPY . .

# Build from the root - this ensures all dependencies are resolved correctly
# Initialize git to satisfy buildnumber plugin
RUN git init && \
    git config user.email "build@inception" && \
    git config user.name "INCEpTION Builder" && \
    git add . && \
    git commit -m "Initial commit for Docker build" 2>/dev/null || true

# Build the project - this will build dependencies first
RUN mvn clean install -DskipTests -B -Dcheckstyle.skip=true -Dmaven.test.failure.ignore=true -T 4 -DbuildNumber=0000000 -Dtimestamp=2024.01.01 -pl inception/inception-app-webapp -am

# Extract the webapp JAR
WORKDIR /app/inception/inception-app-webapp/target
RUN find . -name "*-standalone.jar" -exec cp {} /app/target.jar \;

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre AS runtime

# Define application directory
WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Create application user
RUN groupadd --system --gid 10000 appgroup && \
    useradd --system --uid 10000 --gid appgroup --shell /bin/bash --home /app --create-home appuser

# Copy the built JAR from builder stage
COPY --from=builder /app/target.jar /app/app.jar
COPY --from=builder /app/target.jar /app/data/target.jar

# Create data directory
RUN mkdir -p /app/data && \
    chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose the internal port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/ || exit 1

# Set environment variables
ENV JAVA_OPTS="-XX:+UseZGC -XX:+UnlockExperimentalVMOptions -XX:+UseTransparentHugePages"
ENV JAVA_MEM_OPTS="-XX:MaxRAMPercentage=80"
ENV inception.home=/app/data

# Launch application
CMD ["java", "-jar", "app.jar"]