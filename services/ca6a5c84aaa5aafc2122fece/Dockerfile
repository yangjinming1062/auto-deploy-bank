# Runtime image
FROM docker.io/eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install curl for healthcheck
RUN apk add --no-cache curl

# Copy the built JAR file (renamed to app.jar)
COPY target.jar app.jar

# Expose the application port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]