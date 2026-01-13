FROM eclipse-temurin:8-jre

# Set working directory
WORKDIR /app

# Install wget for health checks
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Copy JAR and configuration
COPY xxl-job-admin-2.3.0-SNAPSHOT.jar /app/xxl-job.jar
COPY application.properties /app/application.properties

# Expose the application port
EXPOSE 9001

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:9001/xxl-job-admin || exit 1

# Run the application
CMD ["java", "-jar", "/app/xxl-job.jar", "--spring.config.location=/app/application.properties"]