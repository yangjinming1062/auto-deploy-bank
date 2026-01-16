# Runtime stage - JAR is built on host
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Copy the pre-built shadow JAR
COPY target.jar app.jar

# Expose default Spring Boot port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]