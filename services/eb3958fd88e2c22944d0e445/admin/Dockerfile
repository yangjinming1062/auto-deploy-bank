# Multi-stage build for admin module
# Stage 1: Build the application with Maven
FROM maven:3.6.3-openjdk-8-slim AS builder

# Accept build argument for revision
ARG REVISION=4.3

# Set working directory
WORKDIR /app

# Copy all source code
COPY . .

# Build the admin module from parent directory
RUN mvn clean package -DskipTests -B -pl admin -am -Drevision=${REVISION}

# Stage 2: Create runtime image
FROM eclipse-temurin:8-jre

# Set working directory
WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy JAR from builder stage (use target.jar name for security scanning)
COPY --from=builder /app/admin/target/*.jar target.jar

# Expose the application port
EXPOSE 8000

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/actuator/health || exit 1

# Run the application
CMD ["java", "-jar", "target.jar"]