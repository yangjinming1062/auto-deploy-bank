# Runtime image for OmegaT (Java Swing Desktop Application)
# Uses pre-built JAR to avoid build-time dependency issues

FROM eclipse-temurin:17-jre-alpine AS runtime

# Install Xvfb and dependencies for headless GUI operation
RUN apk add --no-cache \
    xvfb \
    xvfb-run \
    libx11 \
    libxrandr \
    libxext \
    libxrender \
    libxtst \
    libxi \
    fontconfig \
    freetype \
    alsa-lib \
    ttf-freefont \
    bash

# Create non-root user
RUN addgroup -g 1000 appgroup && \
    adduser -u 1000 -G appgroup -s /bin/bash -D appuser

# Set working directory
WORKDIR /home/appuser

# Copy pre-built JAR from host (mounted volume or build context)
# Main JAR for running the application
COPY build/libs/OmegaT.jar /app/OmegaT.jar
# Copy JAR for security scanning (volume mount path at /app/target.jar)
COPY build/libs/OmegaT.jar /app/target.jar

# Create required directories
RUN mkdir -p /home/appuser/docs /home/appuser/scripts /home/appuser/lib && \
    chown -R appuser:appgroup /home/appuser

# Switch to non-root user
USER appuser

# Set environment variables for headless operation
ENV DISPLAY=:99
ENV JAVA_OPTS="-Xmx1024m"

# Reset entrypoint to avoid base image entrypoint issues
ENTRYPOINT []

# Default command runs OmegaT with Xvfb for headless GUI
CMD ["xvfb-run", "-a", "--server-args=-screen 0 1024x768x24", "java", "-jar", "-Xmx1024m", "/app/OmegaT.jar"]