# Multi-stage build for OpenBoxes Grails application
# This Dockerfile supports both building inside the container and using a pre-built WAR file

# Stage 1: Builder - Build the WAR file using Gradle (for in-container builds)
FROM eclipse-temurin:8-jdk-alpine AS builder

# Install Node.js and npm for frontend build (using project gradle wrapper)
RUN apk add --no-cache nodejs npm

WORKDIR /build

# Copy project files
COPY . .

# Build the WAR file using gradle wrapper (skip tests, git-properties, and npm tasks)
# The npm/node tasks are skipped because the bundle files should be pre-built
RUN chmod +x gradlew && \
    ./gradlew clean build -x test -x integrationTest -x generateGitProperties \
    -x npm_run_bundle -x npmSetup -x nodeSetup \
    -x npmInstall -x npm_run_test -x npm_run_lint \
    -Dorg.gradle.daemon=false \
    --no-daemon

# Stage 2: Runtime - Run the WAR file
FROM eclipse-temurin:8-jre-alpine

LABEL maintainer="support@openboxes.com"
EXPOSE 8080

# Install curl and wget for healthcheck
RUN apk add --no-cache curl bash wget

# Default flags for the JVM. These can be replaced at the runtime.
ENV JAVA_TOOL_OPTIONS="-Xms1024m -Xmx1024m -XX:+UseParallelGC -Djava.awt.headless=true"

# Create openboxes user and group
RUN addgroup -S openboxes && adduser -S -G openboxes -h /app -s /bin/sh openboxes
WORKDIR /app

# Create and chown 'uploads' directory for the OB app
RUN mkdir -p uploads && chown openboxes:openboxes uploads/

# Copy WAR file from builder stage (to /app/openboxes.war)
COPY --from=builder /build/build/libs/openboxes.war /app/openboxes.war
# Also copy to target.jar for security scanning volume mount
COPY --from=builder /build/build/libs/openboxes.war /app/target.jar

USER openboxes

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl --fail http://localhost:8080/openboxes/ || exit 1

CMD ["java", "-Dgrails.env=prod", "-jar", "/app/openboxes.war"]