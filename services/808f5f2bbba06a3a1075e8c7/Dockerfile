# Stage 1: Builder
FROM eclipse-temurin:17-jdk-alpine AS builder

WORKDIR /app

# Install Gradle wrapper dependencies
RUN apk add --no-cache bash

# Copy build configuration files first for better caching
COPY build.gradle ./

# Copy lib directory for local Maven repository and JAR dependencies
COPY lib ./lib

# Copy Gradle wrapper
COPY gradle ./gradle
COPY gradlew ./
COPY gradlew.bat ./
RUN chmod +x gradlew

# Download dependencies and build the project
RUN ./gradlew dependencies --no-daemon

# Copy source code
COPY src ./src

RUN ./gradlew clean assemble --no-daemon -x test

# Copy distro directory for config (needed at runtime)
COPY distro ./distro

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install Python for web server
RUN apk add --no-cache python3

# Create directory for security scanning output
RUN mkdir -p /scan

# Copy the main application JAR to bin directory
# This ensures findInstallDir() returns /app when JAR is at /app/bin/p2rank.jar
COPY --from=builder /app/build/bin/p2rank.jar ./bin/p2rank.jar

# Copy all dependencies to bin/lib
COPY --from=builder /app/distro/bin/lib ./bin/lib

# Copy configuration files
COPY --from=builder /app/distro/config ./config

# Create symlink for security scanning
RUN ln -sf /app/bin/p2rank.jar /app/target.jar

# Copy entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV JAVA_OPTS="-Xmx6G"
ENV POCKET_RANK_BASE_DIR=/app
ENV JAVA_LOCALENV_PARAMS="-Xmx4G"
ENV PRANK_LOCALENV_PARAMS="-threads 4"

# Expose web server port
EXPOSE 8080

# Run the application
ENTRYPOINT ["/docker-entrypoint.sh"]