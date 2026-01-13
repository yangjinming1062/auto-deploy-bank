# Multi-stage build for CRMEB Java Admin application
# Stage 1: Build the application with Maven
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy parent POM and all modules from crmeb directory
COPY crmeb/pom.xml .
COPY crmeb/crmeb-service ./crmeb-service
COPY crmeb/crmeb-common ./crmeb-common
COPY crmeb/crmeb-admin ./crmeb-admin
COPY crmeb/crmeb-front ./crmeb-front

# Build the admin module (skips tests)
RUN mvn clean package -DskipTests -B

# Stage 2: Create runtime image
FROM eclipse-temurin:8-jre-alpine

WORKDIR /app

# Create target directory for JAR mounting
RUN mkdir -p /app/target

# Copy the built JAR from builder stage
COPY --from=builder /app/crmeb-admin/target/Crmeb-admin.jar /app/target.jar

# Expose the internal port (8080)
EXPOSE 8080

# Health check - check if server responds (any HTTP response)
HEALTHCHECK --interval=30s --timeout=10s --start-period=180s --retries=5 \
  CMD nc -z localhost 8080 || exit 0

# Start the application
CMD ["java", "-jar", "/app/target.jar", "--server.port=8081"]