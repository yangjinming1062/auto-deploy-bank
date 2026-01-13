# Security Scanning Dockerfile
# This Dockerfile extracts the built JAR for security scanning

FROM eclipse-temurin:8-jre

WORKDIR /scanner

# Copy the built JAR file from admin module
COPY admin/target/*.jar app.jar

# Tag with scanner for easy identification
LABEL scanner="security-scan"

# This container is used for security scanning only
# The actual application runs via docker-compose with the admin service