# Stage 1: Builder - Compile and build Gradle plugin JARs
FROM amazoncorretto:8-alpine AS builder

# Set working directory
WORKDIR /app

# Copy Gradle wrapper and build files first for better caching
COPY gradlew ./
COPY gradle.properties ./
COPY build.gradle ./
COPY settings.gradle ./
COPY gradle ./gradle/

# Copy source code
COPY . .

# Fix build.gradle to remove deprecated bintray plugins that depend on dead JCenter
RUN sed -i "s/classpath 'com.novoda:bintray-release:0.8.0'/\/\/ classpath 'com.novoda:bintray-release:0.8.0' \/\/ Disabled - JCenter deprecated/" build.gradle && \
    sed -i "s/classpath \"com.jfrog.bintray.gradle:gradle-bintray-plugin:1.8.3\"/\/\/ classpath \"com.jfrog.bintray.gradle:gradle-bintray-plugin:1.8.3\" \/\/ Disabled - JCenter deprecated/" build.gradle && \
    sed -i "s/classpath \"digital.wup:android-maven-publish:3.6.3\"/\/\/ classpath \"digital.wup:android-maven-publish:3.6.3\" \/\/ Disabled/" build.gradle

# Exclude Android-dependent modules (coverage-lib, coverage-plugin, example)
# These modules require Android SDK which is not available in the container
RUN sed -i "s/include ':coverage-plugin'/\/\/ include ':coverage-plugin'/" settings.gradle && \
    sed -i "s/include ':coverage-lib'/\/\/ include ':coverage-lib'/" settings.gradle && \
    sed -i "s/include ':example'/\/\/ include ':example'/" settings.gradle && \
    sed -i "s/project(':coverage-plugin')/\/\/ project(':coverage-plugin')/" settings.gradle && \
    sed -i "s/project(':coverage-lib')/\/\/ project(':coverage-lib')/" settings.gradle && \
    sed -i "s/apply plugin: 'digital.wup.android-maven-publish'/\/\/ apply plugin: 'digital.wup.android-maven-publish' \/\/ Disabled/" gradle/publish-bintray.gradle && \
    sed -i "s/apply plugin: 'com.jfrog.bintray'/\/\/ apply plugin: 'com.jfrog.bintray' \/\/ Disabled/" gradle/publish-bintray.gradle && \
    sed -i "65,91s/^/\/\/ /" gradle/publish-bintray.gradle && \
    sed -i "92,110s/^/\/\/ /" gradle/publish-bintray.gradle

# Make gradlew executable and run build (excluding Android SDK dependent modules)
RUN chmod +x gradlew && ./gradlew assemble --no-daemon -q

# Stage 2: Runtime - Minimal image with built artifacts
FROM amazoncorretto:8-alpine

# Install busybox-extras for httpd server
RUN apk add --no-cache busybox-extras

# Expose the HTTP port
EXPOSE 40500

WORKDIR /app

# Copy the built JAR files from builder stage to a build output directory
COPY --from=builder /app/base-plugin/build/libs/*.jar /build/output/base-plugin.jar
COPY --from=builder /app/common/build/libs/*.jar /build/output/common.jar
COPY --from=builder /app/access-inline-plugin/build/libs/*.jar /build/output/access-inline-plugin.jar
COPY --from=builder /app/TransformEngine/build/libs/*.jar /build/output/TransformEngine.jar

# Create index.html to list available JAR files
RUN echo '<!DOCTYPE html><html><head><title>ByteX Gradle Plugin</title></head><body><h1>ByteX Gradle Plugin Repository</h1><ul>' > /app/index.html && \
    ls -1 /build/output/*.jar 2>/dev/null | xargs -I {} echo '<li><a href="/build/output/{0}">{}</a></li>' | sed 's/{0}//g' >> /app/index.html && \
    echo '</ul></body></html>' >> /app/index.html

# Create target.jar for security scanning during container startup
# This allows the volume mount to work correctly
# Start busybox HTTP server on port 40500, bind to all interfaces
CMD cat /build/output/base-plugin.jar > /app/target.jar 2>/dev/null || cp /build/output/base-plugin.jar /app/target.jar; cp /build/output/*.jar /app/; httpd -f -p 0.0.0.0:40500