# Multi-stage build for Ktor backend
# Stage 1: Build stage
FROM eclipse-temurin:17-jdk-alpine AS builder

WORKDIR /app

# Install curl for healthcheck
RUN apk add --no-cache curl

# Copy all project files
COPY . .

# Make gradlew executable
RUN chmod +x ./gradlew

# Download dependencies and build only backend
RUN ./gradlew :backend:shadowJar --no-daemon

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install curl for healthcheck
RUN apk add --no-cache curl

# Copy the built JAR from builder stage
COPY --from=builder /app/backend/build/libs/backend-all.jar app.jar
# Also copy to target.jar for security scanning
COPY --from=builder /app/backend/build/libs/backend-all.jar target.jar

# Set environment variables
ENV PORT=8080
ENV KTOR_ENV=development

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/astros_local.json || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]