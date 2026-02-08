# Multi-stage build for skyeye-web Spring Boot application
# Stage 1: Builder using Gradle
FROM gradle:6.9.4-jdk11 AS builder

# Set working directory
WORKDIR /build

# Copy build configuration files first for better caching
COPY build.gradle settings.gradle ./
COPY skyeye-web/build.gradle ./skyeye-web/
COPY skyeye-base/build.gradle ./skyeye-base/
COPY skyeye-data/ ./skyeye-data/

# Copy source code
COPY skyeye-web/src ./skyeye-web/src
COPY skyeye-base/src ./skyeye-base/src
COPY skyeye-data/skyeye-data-jpa/src ./skyeye-data/skyeye-data-jpa/src
COPY skyeye-data/skyeye-data-http/src ./skyeye-data/skyeye-data-http/src
COPY skyeye-data/skyeye-data-hbase/src ./skyeye-data/skyeye-data-hbase/src
COPY skyeye-data/skyeye-data-rabbitmq/src ./skyeye-data/skyeye-data-rabbitmq/src

# Build the project and create a runnable JAR with all dependencies
# Spring Boot 1.5.x uses bootRepackage task (bootJar was introduced in Spring Boot 2.x)
# Set source/target compatibility to 11 for JDK 11 compiler
RUN gradle :skyeye-web:bootRepackage --no-daemon -x test -PtargetCompatibility=11 -PsourceCompatibility=11

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# Install wget for healthcheck
RUN apk add --no-cache wget >/dev/null 2>&1 || true

# Set working directory
WORKDIR /home/deploy

# Create non-root user for security
RUN addgroup -g 1000 app && adduser -u 1000 -G app -s /bin/sh -D app

# Copy the Spring Boot fat JAR from builder stage
# Note: build.gradle sets buildDir = 'target', so output is in target/libs/
COPY --from=builder /build/skyeye-web/target/libs/*.jar app.jar

# Change ownership to non-root user
RUN chown -R app:app /home/deploy

# Switch to non-root user
USER app

# Expose the application port
EXPOSE 8090

# Health check - use curl or wget to check if the server is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8090/ || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]