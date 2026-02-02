# Runtime image only - WAR file is built on host
FROM eclipse-temurin:8-jre-alpine

WORKDIR /app

# Copy the pre-built WAR file from host context
COPY target/wego-0.0.1-SNAPSHOT.war wego.war

# Expose the application port
EXPOSE 8081

# Run the application
CMD ["java", "-jar", "wego.war"]