# Multi-stage build for JabRef HTTP Server
# Stage 1: Build the application using Gradle
FROM gradle:8-jdk21-noble AS build

WORKDIR /build

# Copy all source code needed for the build (respecting .dockerignore)
COPY . .

# Create gradle.properties for build
RUN echo "org.gradle.jvmargs=-Xmx4g -XX:+UseG1GC" > /build/gradle.properties

# Build the jabsrv-cli module with installDist
# Use the default JDK from the gradle image (which is JDK 21)
RUN gradle --no-daemon :jabsrv-cli:clean :jabsrv-cli:installDist

# Stage 2: Runtime image using JDK 24 (matches compiled bytecode version)
FROM eclipse-temurin:24-jre-alpine

WORKDIR /app

# Copy the distribution from build stage
COPY --from=build /build/jabsrv-cli/build/install/jabsrv-cli /app

# Install wget for health check
RUN apk add --no-cache wget

# Create a custom startup script using classpath (non-module approach)
RUN echo '#!/bin/sh' > /app/start.sh && \
    echo 'HOST=${JABSRV_HOST:-0.0.0.0}' >> /app/start.sh && \
    echo 'exec java -Xms512m -Xmx2g -cp "/app/lib/*" org.jabref.http.server.cli.ServerCli --host "$HOST" "$@"' >> /app/start.sh && \
    chmod +x /app/start.sh

EXPOSE 23119

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:23119/api/ || exit 1

# Run the server using custom script
CMD ["/app/start.sh"]