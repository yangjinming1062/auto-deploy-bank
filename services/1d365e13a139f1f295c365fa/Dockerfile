# Multi-stage build for Reactor Netty project
# Stage 1: Build stage with Gradle
FROM eclipse-temurin:17-jdk AS builder

# Install JDK 8 and 11 for multi-release JAR compilation
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk openjdk-11-jdk && \
    update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-8-openjdk-amd64/bin/java 1 && \
    update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-11-openjdk-amd64/bin/java 2

WORKDIR /build

# Copy Gradle files
COPY gradlew .
COPY gradle gradle
COPY build.gradle .
COPY settings.gradle .
COPY gradle.properties .

# Make gradlew executable
RUN chmod +x ./gradlew

# Copy source code and configuration
COPY reactor-netty-core reactor-netty-core
COPY reactor-netty-http reactor-netty-http
COPY reactor-netty-http-brave reactor-netty-http-brave
COPY reactor-netty-quic reactor-netty-quic
COPY reactor-netty-examples reactor-netty-examples
COPY reactor-netty-graalvm-smoke-tests reactor-netty-graalvm-smoke-tests
COPY reactor-netty reactor-netty
COPY docs docs
COPY codequality codequality

# Set JAVA_HOME to use Java 17 as the toolchain
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Build using Java 17 as main toolchain with Java 8 and 11 for older versions
# Build only the examples module with shadowJar (fat JAR)
RUN ./gradlew :reactor-netty-examples:shadowJar --no-daemon \
    -Porg.gradle.java.installations.auto-download=false \
    -Porg.gradle.java.installations.paths=/opt/java/openjdk,/usr/lib/jvm/java-8-openjdk-amd64,/usr/lib/jvm/java-11-openjdk-amd64 \
    -x test

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the shadow JAR (fat JAR) from builder stage
COPY --from=builder /build/reactor-netty-examples/build/libs/reactor-netty-examples-*.jar ./reactor-netty-examples.jar

# Create a copy for security scanning
RUN cp ./reactor-netty-examples.jar ./target.jar

# Expose the application port (HTTP server uses 8080 internally)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/hello || exit 1

# Create entrypoint script to ensure target.jar is available for security scanning
COPY <<'EOF' /entrypoint.sh
#!/bin/sh
# Ensure target.jar exists (it might be mounted over by Docker volume)
# If the mounted file is empty or doesn't contain a valid JAR, copy from the original
if [ ! -s /app/target.jar ] || ! unzip -t /app/target.jar >/dev/null 2>&1; then
  echo "target.jar is empty or invalid, copying from reactor-netty-examples.jar"
  cp /app/reactor-netty-examples.jar /app/target.jar
fi
# Run the HelloWorldServer application (port 8080 is hardcoded in the example)
exec java -jar /app/reactor-netty-examples.jar
EOF

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]