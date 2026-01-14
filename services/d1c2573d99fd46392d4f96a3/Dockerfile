# Stage 1: Build with Gradle and Java 17
FROM gradle:7.6-jdk17 AS builder

WORKDIR /app

# Copy Gradle configuration files
COPY build.gradle settings.gradle gradle.properties ./
COPY gradle ./gradle
COPY shaka/build.gradle shaka/build.gradle
COPY shaka/lib/build.gradle shaka/lib/

# Copy source directories for lib module
COPY shaka/lib/ ./shaka/lib/

# Apply build file patches for Gradle 7.x compatibility
RUN \
    # Fix root build.gradle
    sed -i 's/testCompile/testImplementation/g' build.gradle && \
    sed -i "s/task wrapper(type: Wrapper)/task _wrapper(type: Wrapper)/g" build.gradle && \
    # Fix shaka/build.gradle
    sed -i '/buildscript {/,/^}/d' shaka/build.gradle && \
    sed -i "/apply plugin: 'aspectj'/d" shaka/build.gradle && \
    sed -i '/^subprojects {/,/^}$/d' shaka/build.gradle && \
    sed -i '/configure(subprojects/,/^}/d' shaka/build.gradle && \
    sed -i 's/\bcompile\b/implementation/g' shaka/build.gradle && \
    # Fix lib/build.gradle
    sed -i 's/\bcompile\b/implementation/g' shaka/lib/build.gradle && \
    sed -i '/^processResources {/a\    duplicatesStrategy = DuplicatesStrategy.INCLUDE' shaka/lib/build.gradle && \
    # Add jar task with specific archive name
    echo "" >> shaka/lib/build.gradle && \
    echo "jar {" >> shaka/lib/build.gradle && \
    echo "    archiveFileName = 'ShakaApktool_lib.jar'" >> shaka/lib/build.gradle && \
    echo "}" >> shaka/lib/build.gradle && \
    # Remove AspectJ aspect files
    find shaka -name "*Aj.java" -delete 2>/dev/null || true

# Build the lib module
RUN gradle :shaka:lib:jar --no-daemon -PduplicatesStrategy=WARN && \
    ls -la /app/shaka/lib/build/libs/

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install wget, netcat-openbsd for health check
RUN apk add --no-cache wget netcat-openbsd

# Set JAVA_HOME
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Copy the built JAR to app.jar
COPY --from=builder /app/shaka/lib/build/libs/ShakaApktool_lib.jar /app/app.jar

# Create startup script that copies JAR to volume mount path for security scanning
COPY <<'EOF' /app/start.sh
#!/bin/sh

# Source JAR location (either volume-mounted or built-in)
SOURCE_JAR="/app/app.jar"
# Target path for security scanning (volume-mounted directory)
TARGET_JAR="/app/target.jar"

# Copy JAR to target path for security scanning
if [ -f "$SOURCE_JAR" ]; then
    cp "$SOURCE_JAR" "$TARGET_JAR"
    echo "JAR copied to $TARGET_JAR for security scanning"
    echo "JAR size: $(wc -c < $TARGET_JAR) bytes"
else
    echo "Error: Source JAR not found at $SOURCE_JAR"
    exit 1
fi

# Start HTTP health check server
start_http_server() {
    echo "Service ready on port 8080"
    while true; do
        echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK" | nc -l -p 8080 -q 1
    done
}

start_http_server
EOF
RUN chmod +x /app/start.sh

# Expose the service port
EXPOSE 8080

# Run the startup script
CMD ["/app/start.sh"]