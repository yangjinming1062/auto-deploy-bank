# Stage 2: Runtime image (Alpine-based)
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install curl for health checks (use apk for Alpine)
RUN apk add --no-cache curl

# Create target directory for volume mount
RUN mkdir -p /app/target

# Copy pre-built JAR from context (expected at target.jar in build context)
COPY target.jar app.jar

# Copy JAR to target directory for volume mounting and security scanning
RUN cp /app/app.jar /app/target.jar

# Create directories for application data
RUN mkdir -p /opt/rackshift/logs/rackshift /opt/rackshift/conf

# Expose port
EXPOSE 8082

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=5 \
  CMD curl -f http://localhost:8082/ || exit 1

# Start application
CMD ["java", "-jar", "app.jar"]