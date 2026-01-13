# Multi-stage build for Spring Boot WAR application
FROM eclipse-temurin:17-jdk-alpine AS runtime

LABEL maintainer="Hai Liang Wang <hain@chatopera.com>"

# Create necessary directories
RUN mkdir -p /{data,logs,app}

# Copy the pre-built WAR file
COPY app/target/contact-center.war /app/target.jar

# Set working directory
WORKDIR /app

# Expose HTTP port
EXPOSE 8035

# Run the application
ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", "-Xmx12288m", "-Xms2048m", "-jar", "target.jar"]