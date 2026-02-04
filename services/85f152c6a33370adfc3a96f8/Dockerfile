# Stage 1: Builder - Build the Android APK
FROM eclipse-temurin:17-jdk AS builder

# Install required tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    wget \
    unzip \
    git \
    make \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set Android SDK environment variables
ENV ANDROID_HOME /opt/android-sdk
ENV ANDROID_SDK_ROOT /opt/android-sdk
ENV PATH ${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools

# Download and install Android SDK command line tools
RUN wget -q "https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip" -O /tmp/cmdline-tools.zip && \
    unzip -q /tmp/cmdline-tools.zip -d /opt/android-sdk && \
    mkdir -p /opt/android-sdk/cmdline-tools/latest && \
    mv /opt/android-sdk/cmdline-tools/bin /opt/android-sdk/cmdline-tools/lib /opt/android-sdk/cmdline-tools/latest/ 2>/dev/null || true && \
    rm -f /tmp/cmdline-tools.zip

# Accept licenses and install required SDK components
RUN yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses || true
RUN $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager \
    "platform-tools" \
    "platforms;android-36" \
    "build-tools;36.0.0" \
    "ndk;23.2.8568313" \
    "cmake;4.0.3"

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/85f152c6a33370adfc3a96f8

# Copy project files
COPY . .

# Make gradlew executable
RUN chmod +x ./gradlew

# Clear any problematic environment variables
ENV MAKEFLAGS=""

# Build the project
RUN ./gradlew assembleDebug --no-daemon --stacktrace 2>&1

# Stage 2: Runtime - Copy output artifacts
FROM eclipse-temurin:17-jre-alpine AS runtime

# Install Python for HTTP server
RUN apk add --no-cache python3

# Create directories for outputs
RUN mkdir -p /home/ubuntu/deploy-projects/85f152c6a33370adfc3a96f8/output

# Copy built APK from builder stage
COPY --from=builder /home/ubuntu/deploy-projects/85f152c6a33370adfc3a96f8/app/build/outputs/apk/debug/app-debug.apk /home/ubuntu/deploy-projects/85f152c6a33370adfc3a96f8/output/app-debug.apk

# Also copy to /home/ubuntu/deploy-projects/85f152c6a33370adfc3a96f8/target.jar internal location for security scanning
COPY --from=builder /home/ubuntu/deploy-projects/85f152c6a33370adfc3a96f8/app/build/outputs/apk/debug/app-debug.apk /home/ubuntu/deploy-projects/85f152c6a33370adfc3a96f8/target.jar.internal

# Entrypoint to copy JAR to mounted volume and start HTTP server
COPY <<EOF /entrypoint.sh
#!/bin/sh
cp /home/ubuntu/deploy-projects/85f152c6a33370adfc3a96f8/target.jar.internal /home/ubuntu/deploy-projects/85f152c6a33370adfc3a96f8/target.jar
cd /home/ubuntu/deploy-projects/85f152c6a33370adfc3a96f8
exec python3 -m http.server 41810
EOF
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]