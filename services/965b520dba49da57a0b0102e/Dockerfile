# Stage 1: Build stage
FROM gradle:8.5-jdk17-alpine AS builder

WORKDIR /build

# Copy build configuration files first for better caching
COPY build.gradle.kts settings.gradle.kts gradle.properties ./
COPY gradle ./gradle
COPY common/build.gradle.kts common/build.gradle.kts

# Copy source code
COPY src ./src
COPY common/src ./common/src
COPY module ./module

# Build the application JAR with all modules
RUN gradle :shadowJar --no-daemon -x test

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

# Create non-root user for security
RUN addgroup -g 1000 app && adduser -u 1000 -G app -s /bin/sh -D app

# Set working directory
WORKDIR /home/app

# Copy the built fat JAR to app.jar (this path will be volume mounted for security scanning)
COPY --from=builder /build/build/libs/*.jar app.jar

# Create directories for configuration and data
RUN mkdir -p /data/LifePhoton/prop && chown -R app:app /data/LifePhoton

# Switch to non-root user
USER app

# Expose the application port
EXPOSE 808

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:808/ || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]