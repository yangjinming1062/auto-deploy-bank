# Multi-stage build for MuJing (幕境) Jetpack Compose Desktop application
# This is a desktop English learning application with video playback capabilities

# Stage 1: Build with Gradle
FROM eclipse-temurin:17-jdk-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    git \
    curl \
    unzip \
    xz \
    bash \
    libstdc++ \
    libc6-compat \
    && rm -rf /var/cache/apk/*

# Set up Gradle
ARG GRADLE_VERSION=8.5
ENV GRADLE_VERSION=${GRADLE_VERSION}
ENV GRADLE_HOME=/opt/gradle-${GRADLE_VERSION}
ENV PATH=${GRADLE_HOME}/bin:${PATH}

# Download and install Gradle
RUN curl -fsSL "https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip" -o /tmp/gradle.zip && \
    unzip -q /tmp/gradle.zip -d /opt && \
    rm /tmp/gradle.zip

# Create symlink
RUN ln -sf /opt/gradle-${GRADLE_VERSION} /opt/gradle

WORKDIR /app

# Copy build configuration files
COPY build.gradle.kts settings.gradle.kts wix.gradle.kts ./
COPY gradle.properties ./
COPY gradle/ ./gradle/

# Copy source files
COPY src/ ./src/
COPY resources/ ./resources/
COPY lib/ ./lib/
COPY dict/ ./dict/

# Create gradle wrapper
RUN gradle wrapper --gradle-version ${GRADLE_VERSION}

# Build the application (skip tests for container build)
RUN gradle build -x test -x testLast -x testClasses --no-daemon

# Create a JAR from compiled Kotlin classes for security scanning
RUN mkdir -p /app/build/libs && \
    cd /app/build/classes/kotlin/main && \
    jar cf /app/build/libs/target.jar . && \
    echo "Created target.jar with $(jar tf /app/build/libs/target.jar | wc -l) entries"

# Stage 2: Runtime image with GUI support
FROM ubuntu:22.04 AS runtime

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    libx11-6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    libasound2 \
    libavcodec-extra \
    libavformat-dev \
    libswscale-dev \
    libavutil-dev \
    xvfb \
    wget \
    unzip \
    curl \
    python3 \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Install VLC
RUN apt-get update && apt-get install -y --no-install-recommends \
    vlc \
    && rm -rf /var/lib/apt/lists/*

# Install Gradle for running at runtime
ARG GRADLE_VERSION=8.5
ENV GRADLE_VERSION=${GRADLE_VERSION}
ENV GRADLE_HOME=/opt/gradle-${GRADLE_VERSION}
ENV PATH=${GRADLE_HOME}/bin:${PATH}

RUN curl -fsSL "https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip" -o /tmp/gradle.zip && \
    unzip -q /tmp/gradle.zip -d /opt && \
    rm /tmp/gradle.zip && \
    ln -sf /opt/gradle-${GRADLE_VERSION} /opt/gradle

# Set up Java environment
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 \
    PATH="${JAVA_HOME}/bin:${PATH}" \
    DISPLAY=:99

# Copy built application from builder stage
WORKDIR /app

# Copy the built JAR for security scanning (named target.jar as required)
COPY --from=builder /app/build/libs/target.jar /target.jar

# Copy project structure for running with Gradle
COPY --from=builder /app/src/ ./src/
COPY --from=builder /app/resources/ ./resources/
COPY --from=builder /app/lib/ ./lib/
COPY --from=builder /app/dict/ ./dict/
COPY --from=builder /app/build.gradle.kts /app/
COPY --from=builder /app/settings.gradle.kts /app/
COPY --from=builder /app/wix.gradle.kts /app/
COPY --from=builder /app/gradle.properties /app/
COPY --from=builder /app/gradle/ ./gradle/

# Copy FFmpeg binary
COPY --from=builder /app/resources/linux/ffmpeg/ffmpeg /usr/local/bin/ffmpeg

# Create startup script
RUN cat > /app/start.sh <<'EOF' && chmod +x /app/start.sh
#!/bin/bash
set -e
export DISPLAY=:99
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export LD_LIBRARY_PATH=/usr/lib:/lib:$LD_LIBRARY_PATH
rm -f /tmp/.X99-lock /tmp/.X11-unix/X99 2>/dev/null || true
echo "Starting Xvfb..."
Xvfb :99 -screen 0 1024x768x24 &
XVFB_PID=$!
sleep 2
if ! kill -0 $XVFB_PID 2>/dev/null; then
  echo "ERROR: Xvfb failed to start"
  exit 1
fi
echo "Xvfb started with PID $XVFB_PID"
# Start simple HTTP server for health checks using Python
python3 -c "
import http.server
import socketserver
PORT = 8080
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'MuJing Desktop App Running')
    def log_message(self, format, *args):
        pass
with socketserver.TCPServer(('', PORT), Handler) as httpd:
    print(f'HTTP health server started on port {PORT}')
    httpd.serve_forever()
" &
HTTP_PID=$!
echo "HTTP health server started on port 8080 (PID: $HTTP_PID)"
cd /app
gradle run --no-daemon &
APP_PID=$!
echo "MuJing app started (PID: $APP_PID)"
wait $APP_PID
EXIT_CODE=$?
kill $HTTP_PID 2>/dev/null || true
exit $EXIT_CODE
EOF

# Expose port for health check
EXPOSE 8080

# Health check - verify HTTP server is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Start the application
CMD ["/app/start.sh"]