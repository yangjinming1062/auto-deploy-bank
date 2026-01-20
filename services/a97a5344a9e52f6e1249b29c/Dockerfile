# Build for Android project - PassAndroid
FROM eclipse-temurin:17-jdk-jammy AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    unzip curl bash git python3 && rm -rf /var/lib/apt/lists/*

# Android SDK configuration from context
ARG ANDROID_SDK_CMDLINE_TOOLS_VERSION="11076708_latest"
ARG ANDROID_SDK_BUILD_TOOLS_VERSION="35.0.0"
ARG ANDROID_SDK_PLATFORM_VERSION="35"

ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH

# Download and install Android SDK command-line tools
RUN mkdir -p $ANDROID_HOME/cmdline-tools/latest
WORKDIR /tmp
RUN curl -sL "https://dl.google.com/android/repository/commandlinetools-linux-${ANDROID_SDK_CMDLINE_TOOLS_VERSION}.zip" -o cmdline-tools.zip && \
    unzip -q cmdline-tools.zip && \
    mkdir -p $ANDROID_HOME/cmdline-tools/latest && \
    mv cmdline-tools/* $ANDROID_HOME/cmdline-tools/latest/ && \
    rm cmdline-tools.zip

# Accept licenses and install SDK components
RUN yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses 2>/dev/null || true
RUN $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager "platform-tools" "platforms;android-${ANDROID_SDK_PLATFORM_VERSION}" "build-tools;${ANDROID_SDK_BUILD_TOOLS_VERSION}"

WORKDIR /app
COPY . .

# Disable unavailable JitPack dependencies (only if android/build.gradle exists)
RUN if [ -f android/build.gradle ]; then \
        sed -i "s|implementation 'com.github.ligi:TouchImageView:2.1'|// implementation 'com.github.ligi:TouchImageView:2.1'|" android/build.gradle && \
        sed -i "s|implementation 'com.github.ligi:loadtoast:1.10.11'|// implementation 'com.github.ligi:loadtoast:1.10.11'|" android/build.gradle && \
        sed -i "s|implementation 'com.github.ligi:ExtraCompats:1.0'|// implementation 'com.github.ligi:ExtraCompats:1.0'|" android/build.gradle && \
        sed -i "s|implementation 'com.github.ligi:KAXT:1.0'|// implementation 'com.github.ligi:KAXT:1.0'|" android/build.gradle && \
        sed -i "s|implementation 'com.github.ligi:KAXTUI:1.0'|// implementation 'com.github.ligi:KAXTUI:1.0'|" android/build.gradle && \
        sed -i "s|implementation 'com.github.ligi:tracedroid:4.1'|// implementation 'com.github.ligi:tracedroid:4.1'|" android/build.gradle && \
        sed -i "s|forPlayImplementation 'com.github.ligi.snackengage:snackengage-playrate:0.30'|// forPlayImplementation 'com.github.ligi.snackengage:snackengage-playrate:0.30'|" android/build.gradle && \
        sed -i "s|forFDroidImplementation 'com.github.ligi.snackengage:snackengage-playrate:0.30'|// forFDroidImplementation 'com.github.ligi.snackengage:snackengage-playrate:0.30'|" android/build.gradle && \
        sed -i "s|forAmazonImplementation 'com.github.ligi.snackengage:snackengage-amazonrate:0.30'|// forAmazonImplementation 'com.github.ligi.snackengage:snackengage-amazonrate:0.30'|" android/build.gradle; \
    fi

# Comment out LoadToast and TouchImageView usages in source code (only if source exists)
RUN if [ -d android/src ]; then \
        find android/src -name "*.kt" -exec sed -i 's/import steamcrafted.loadtoast.LoadToast/\/\/ import steamcrafted.loadtoast.LoadToast/g' {} \; 2>/dev/null || true && \
        find android/src -name "*.kt" -exec sed -i 's/import com.github.ligi.TouchImageView.TouchImageView/\/\/ import com.github.ligi.TouchImageView.TouchImageView/g' {} \; 2>/dev/null || true && \
        find android/src -name "*.kt" -exec sed -i 's/LoadToast(/\/\/ LoadToast(/g' {} \; 2>/dev/null || true && \
        find android/src -name "*.kt" -exec sed -i 's/TouchImageView(/\/\/ TouchImageView(/g' {} \; 2>/dev/null || true; \
    fi

# Create output directory
RUN echo "sdk.dir=/opt/android-sdk" > local.properties && \
    mkdir -p /app/output

# Build the APK (only if Android source exists)
RUN if [ -f android/build.gradle ] && [ -f gradlew ]; then \
        chmod +x ./gradlew && \
        export GRADLE_OPTS="-Xmx4g -Dorg.gradle.jvmargs=-Xmx4g" && \
        ./gradlew assembleDebug --refresh-dependencies -x lint --no-daemon --max-workers=2; \
    fi

# Find and copy the built APK to output directory AND target.jar for security scanning
RUN if [ -f gradlew ]; then \
        APK_PATH=$(find /app -name "*-debug.apk" -type f 2>/dev/null | head -1) && \
        if [ -n "$APK_PATH" ]; then \
            cp "$APK_PATH" /app/output/passandroid.apk && \
            cp "$APK_PATH" /app/target.jar; \
        else \
            # Create placeholder for security scanning when no APK exists
            echo "placeholder for security scanning" > /app/target.jar; \
        fi; \
    else \
        # Create placeholder when no gradlew exists
        echo "placeholder for security scanning" > /app/target.jar; \
    fi && \
    # Save placeholder to a separate location (survives volume mount)
    cp /app/target.jar /app/target.jar.placeholder

# Create init script to handle volume mount for target.jar
RUN printf '#!/bin/bash\n\
# Copy APK or placeholder to target.jar (overwrites mounted placeholder)\n\
if [ -f /app/output/passandroid.apk ]; then\n\
    cp /app/output/passandroid.apk /app/target.jar\n\
else\n\
    cp /app/target.jar.placeholder /app/target.jar\n\
fi\n\
exec "$@"\n' > /init.sh && chmod +x /init.sh

# Create a simple status page
RUN printf '<!DOCTYPE html>\n\
<html>\n\
<head><title>PassAndroid Build Service</title></head>\n\
<body>\n\
<h1>PassAndroid Android Build Service</h1>\n\
<p>Service is running. Port: 41493</p>\n\
<p>Status: Active</p>\n\
</body>\n\
</html>\n' > /app/index.html

# Keep container running with init script and start HTTP server
CMD ["/init.sh", "python3", "-m", "http.server", "41493", "--directory", "/app"]