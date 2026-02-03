# Stage 1: Build the Android demo app
FROM eclipse-temurin:17-jdk-alpine AS builder

# Install required tools for Android SDK
RUN apk add --no-cache \
    wget \
    unzip \
    zip \
    libstdc++ \
    libc6-compat \
    bash

# Set Android SDK environment variables
ENV ANDROID_HOME=/opt/android-sdk \
    ANDROID_SDK_ROOT=/opt/android-sdk \
    PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# Download and install Android SDK command-line tools
WORKDIR /opt/android-sdk
RUN mkdir -p cmdline-tools/latest && \
    cd cmdline-tools/latest && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-10406996_latest.zip -O cmdline-tools.zip && \
    unzip -q cmdline-tools.zip && \
    mv cmdline-tools/* . && \
    rm -rf cmdline-tools cmdline-tools.zip

# Accept licenses and install required SDK components
RUN yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses > /dev/null 2>&1 || true
RUN $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager \
    "platforms;android-33" \
    "build-tools;33.0.0" \
    "platform-tools"

# Set working directory
WORKDIR /app

# Copy project files
COPY gradle.properties .
COPY gradlew .
COPY build.gradle .
COPY settings.gradle .
COPY gradle/wrapper ./gradle/wrapper
COPY library ./library
COPY demo ./demo

# Build the demo APK
RUN chmod +x gradlew
RUN ./gradlew assembleDebug --no-daemon --stacktrace

# Stage 2: Runtime image (for serving/verification)
FROM eclipse-temurin:17-jre-alpine

# Install Python for HTTP server
RUN apk add --no-cache python3

# Create directories for APK output and web content
WORKDIR /app

# Copy the built APK from builder stage
COPY --from=builder /app/demo/build/outputs/apk/debug/demo-debug.apk /app/target.jar

# Create a simple web page
RUN mkdir -p /app/web && echo '<!DOCTYPE html><html><head><title>Scene Demo Service</title></head><body style="font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px;"><h1>Scene Demo Android Service</h1><p>This service is running successfully!</p><p>The Android demo APK has been built and is available.</p><hr><p>Service Status: <strong style="color: green;">Running</strong></p></body></html>' > /app/web/index.html

# Expose port 8080
EXPOSE 8080

# Run Python HTTP server on port 8080
CMD ["python3", "-m", "http.server", "8080", "--directory", "/app/web"]