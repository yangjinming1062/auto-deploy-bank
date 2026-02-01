# Multi-stage build for Android Gradle project
FROM eclipse-temurin:11-jdk AS builder

# Install necessary tools
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set Android SDK version and NDK version
ENV ANDROID_SDK_VERSION "29"
ENV ANDROID_NDK_VERSION "21.4.7075529"

# Set environment variables for Android SDK/NDK
ENV ANDROID_HOME "/opt/android-sdk"
ENV ANDROID_SDK_ROOT "/opt/android-sdk"
ENV ANDROID_NDK_ROOT "/opt/android-sdk/ndk/${ANDROID_NDK_VERSION}"
ENV PATH "${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools"

# Download and install Android SDK command-line tools
RUN mkdir -p "${ANDROID_HOME}/cmdline-tools" && \
    cd "${ANDROID_HOME}/cmdline-tools" && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O cmdline-tools.zip && \
    unzip -q cmdline-tools.zip && \
    mv cmdline-tools latest && \
    rm cmdline-tools.zip

# Accept licenses and install required SDK components
RUN yes | "${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager" --licenses || true && \
    "${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager" \
        "platforms;android-${ANDROID_SDK_VERSION}" \
        "build-tools;29.0.3" \
        "ndk;${ANDROID_NDK_VERSION}"

# Set working directory
WORKDIR /app

# Copy Gradle wrapper and build files first for caching
COPY gradle/wrapper/ gradle/wrapper/
COPY gradlew ./
COPY gradle.properties ./
COPY build.gradle ./
COPY settings.gradle ./

# Update Gradle wrapper to version 7.3.3 for better compatibility with Java 11
RUN sed -i 's|gradle-6.7.1-all.zip|gradle-7.3.3-all.zip|g' gradle/wrapper/gradle-wrapper.properties

# Replace deprecated jcenter() with proper repositories in build.gradle
# Rewrite build.gradle with correct repository configuration
RUN printf "buildscript {\n    repositories {\n        maven { url 'https://maven.google.com' }\n        google()\n        mavenCentral()\n    }\n    dependencies {\n        classpath 'com.android.tools.build:gradle:4.2.2'\n    }\n}\n\nallprojects {\n    repositories {\n        maven { url 'https://maven.google.com' }\n        google()\n        mavenCentral()\n        maven { url 'https://jitpack.io' }\n    }\n}\n" > build.gradle

# Update settings.gradle to add pluginManagement for Google repository at the beginning
RUN printf 'pluginManagement {\n    repositories {\n        google()\n        mavenCentral()\n        gradlePluginPortal()\n    }\n}\n\n' > settings.gradle.tmp && \
    cat settings.gradle >> settings.gradle.tmp && \
    mv settings.gradle.tmp settings.gradle

COPY demo/ demo/
COPY library/ library/

# Make gradlew executable
RUN chmod +x gradlew

# Build the project (assembleRelease for library module)
RUN ./gradlew :library:assembleRelease --no-daemon

# Copy the built AAR file to the expected JAR location for security scanning
RUN cp library/build/outputs/aar/library-release.aar /app/target.jar

# Runtime stage - minimal image for extracting artifacts
FROM eclipse-temurin:11-jre-alpine AS runtime

# Install Python for HTTP server
RUN apk add --no-cache python3

# Copy the built artifact from builder to a fixed location
COPY --from=builder /app/target.jar /app/built-artifact.jar

# Create output directory for additional artifacts
RUN mkdir -p /app/output

# Create a simple status page
RUN printf '<!DOCTYPE html><html><head><title>Android Builder Service</title></head><body><h1>Android Builder Service</h1><p>Container is running successfully.</p><p>Built artifacts are available at /app/target.jar</p></body></html>' > /app/index.html

# Entrypoint to copy artifact to mounted volume location and start HTTP server
RUN printf '#!/bin/sh\ncp /app/built-artifact.jar /app/target.jar\ncd /app && exec python3 -m http.server 43794\n' > /entrypoint.sh && chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["bash"]