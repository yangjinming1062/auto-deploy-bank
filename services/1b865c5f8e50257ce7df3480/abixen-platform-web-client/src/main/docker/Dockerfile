# Multi-stage build for Abixen Platform Web Client
# Stage 1: Builder
FROM maven:3.8-eclipse-temurin-8 AS builder

# Copy the entire project
COPY . /app/

# Install the common module first
WORKDIR /app/abixen-platform-common
RUN mvn install -DskipTests -B

# Build the web-client module
WORKDIR /app/abixen-platform-web-client
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:8-jre

WORKDIR /app

# Copy WAR from builder stage
COPY --from=builder /app/abixen-platform-web-client/target/abixen-platform.war app.war

# Expose port 8080
EXPOSE 8080

# Set the entrypoint
ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", "-Dspring.profiles.active=docker", "-Dabixen.services.eureka.uri=discovery", "-Dabixen.services.gateway.uri=gateway", "-jar", "app.war"]
