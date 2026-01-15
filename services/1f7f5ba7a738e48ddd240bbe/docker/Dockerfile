# Multi-stage build for OpenBoxes Grails application
# This Dockerfile supports both building inside the container and using a pre-built WAR file

# Stage 1: Builder - Build the WAR file using Gradle (for in-container builds)
FROM eclipse-temurin:8-jdk-alpine AS builder

# Install Gradle, Node.js, and npm for frontend build
RUN apk add --no-cache gradle nodejs npm

WORKDIR /build

# Copy project files
COPY . .

# Build the WAR file (skip tests for production build)
RUN gradle clean build -x test -x integrationTest --no-daemon

# Stage 2: Runtime - Run the WAR file
FROM eclipse-temurin:8-jre-alpine

LABEL maintainer="support@openboxes.com"
EXPOSE 8080

# Install curl for healthcheck
RUN apk add --no-cache curl bash

# Default flags for the JVM. These can be replaced at the runtime.
ENV JAVA_TOOL_OPTIONS="-Xms1024m -Xmx1024m -XX:+UseParallelGC -Djava.awt.headless=true"

# Create openboxes user and group
RUN addgroup -S openboxes && adduser -S -G openboxes -h /app -s /bin/sh openboxes
WORKDIR /app

# Create and chown 'uploads' directory for the OB app
RUN mkdir -p uploads && chown openboxes:openboxes uploads/

# Use pre-built WAR file from mount if available, otherwise use builder stage
# The volume mount provides the WAR file at /app/target.war for security scanning
COPY --from=builder /build/build/libs/openboxes.war openboxes.war

USER openboxes

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl --fail http://localhost:8080/openboxes/health || exit 1

CMD ["java", "-Dgrails.env=prod", "-jar", "/app/openboxes.war"]
