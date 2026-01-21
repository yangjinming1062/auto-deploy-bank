# Multi-stage build for DevoxxGenie IntelliJ Plugin
# Stage 1: Build the plugin
FROM eclipse-temurin:17-jdk-alpine AS builder

# Install git (required for Gradle wrapper)
RUN apk add --no-cache git

WORKDIR /app

# Copy Gradle wrapper and build configuration files
COPY gradlew .
COPY gradle/ gradle/
COPY gradle.properties .
COPY settings.gradle.kts .
COPY build.gradle.kts .

# Make gradlew executable
RUN chmod +x ./gradlew

# Copy source code and resources
COPY src/ src/
COPY core/ core/

# Build the plugin using shadowJar (produces target.jar)
RUN ./gradlew shadowJar --no-daemon --console=plain

# Stage 2: Runtime environment (for development)
FROM eclipse-temurin:17-jre-alpine AS runtime

WORKDIR /app

# Copy the built target.jar from builder stage
COPY --from=builder /app/build/libs/target.jar /app/target.jar

# Keep container running for development
CMD ["tail", "-f", "/dev/null"]