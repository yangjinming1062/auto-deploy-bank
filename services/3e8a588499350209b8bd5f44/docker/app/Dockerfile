# Multi-stage build for Tolgee Spring Boot application
# Stage 1: Build with Gradle
FROM eclipse-temurin:21-jdk-alpine AS builder

# Install Gradle
RUN apk add --no-cache curl unzip && \
    GRADLE_VERSION=8.10.2 && \
    curl -fsSL https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip -o /tmp/gradle.zip && \
    unzip -q /tmp/gradle.zip -d /opt && \
    rm /tmp/gradle.zip && \
    ln -s /opt/gradle-${GRADLE_VERSION}/bin/gradle /usr/local/bin/gradle

WORKDIR /app

# Copy project files
COPY . .

# Build the application (skip tests for faster build)
RUN ./gradlew :server-app:bootJar -x test --no-daemon --build-cache

# Extract the bootJar to expected structure for cmd.sh
# The bootJar is created in backend/app/build/libs
WORKDIR /app/backend/app/build/libs
RUN unzip -q *.jar -d /tmp/jar-extract && \
    mkdir -p /app/docker-build && \
    # Move BOOT-INF contents to app directory structure expected by cmd.sh
    mv /tmp/jar-extract/BOOT-INF/classes /app/docker-build/app && \
    mv /tmp/jar-extract/BOOT-INF/lib /app/docker-build/ && \
    mv /tmp/jar-extract/META-INF /app/docker-build/

# Stage 2: Runtime image
FROM eclipse-temurin:21-jre-alpine

# Install required runtime dependencies
RUN apk --no-cache add libxml2 bash

WORKDIR /app

# Copy built artifacts from builder stage
COPY --from=builder /app/docker-build /app

# Copy the startup script from the original source
COPY --chmod=755 docker/app/cmd.sh /app/cmd.sh

# Expose application port
EXPOSE 8080

# Environment variables
ENV HEALTHCHECK_PORT=8080 \
    spring_profiles_active=docker

# Volume for persistent data
VOLUME /data

# Health check
HEALTHCHECK --interval=10s --timeout=3s --retries=20 \
    CMD wget --spider -q "http://127.0.0.1:$HEALTHCHECK_PORT/actuator/health" || exit 1

# Startup command
ENTRYPOINT ["/app/cmd.sh"]