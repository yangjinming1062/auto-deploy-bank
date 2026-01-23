# Stage 1: Build with Gradle
FROM gradle:8.5-jdk17 AS builder

WORKDIR /build

# Copy build configuration files first for better caching
COPY build.gradle settings.gradle gradle.properties ./
COPY build-logic/ build-logic/
COPY vendor/ vendor/
COPY gradle/libs.versions.toml gradle/
COPY core/ core/

# Build the core module (standalone, no vendor dependencies needed)
# Disable auto patch apply as git repo is not available
RUN gradle :core:jar --no-daemon -x test -Pvendor.disableAutoPatchApply=true

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install curl for healthcheck
RUN apk add --no-cache curl

# Copy the built JAR to app.jar
COPY --from=builder /build/core/build/libs/*.jar /app/app.jar

# Create entrypoint script to copy JAR to mounted volume for security scanning
COPY <<'EOF' /entrypoint.sh
#!/bin/sh
# Copy JAR to /app/target for security scanning if the directory is mounted
if [ -d /app/target ]; then
    cp /app/app.jar /app/target/target.jar
fi
exec "$@"
EOF
RUN chmod +x /entrypoint.sh

# Run the JAR via entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD ["java", "-jar", "app.jar"]