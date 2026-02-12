# Runtime image for Quarkus application
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy the pre-built JAR
COPY target.jar app.jar

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose the HTTP port
EXPOSE 8080

# Set environment variables
ENV QUARKUS_HTTP_PORT=8080
ENV QUARKUS_HTTP_HOST=0.0.0.0

# Run the application
CMD ["java", "-jar", "app.jar"]