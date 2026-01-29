# Stage 1: Build with Eclipse Temurin 21 (required by Gradle 9)
FROM eclipse-temurin:21-jdk AS builder

WORKDIR /app

# Install Java 8 for the project build (required by elasticsearch-hadoop)
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-8-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA8_HOME as ENV for the build
ENV JAVA8_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# Copy project files
COPY gradle.properties ./
COPY gradlew ./
COPY gradle/ ./gradle/
COPY buildSrc/ ./buildSrc/
COPY build.gradle ./
COPY settings.gradle ./
COPY mr/ ./mr/
COPY hive/ ./hive/
COPY spark/ ./spark/
COPY dist/ ./dist/
COPY thirdparty/ ./thirdparty/
COPY test/ ./test/
COPY qa/ ./qa/
COPY docs/ ./docs/
COPY licenses/ ./licenses/
COPY NOTICE.txt ./
COPY LICENSE.txt ./
COPY README.md ./

# Configure Gradle to detect Java 8 installation
RUN sed -i 's/org.gradle.java.installations.auto-detect=false/org.gradle.java.installations.auto-detect=true/' gradle.properties && \
    echo "org.gradle.java.installations.paths=$JAVA8_HOME" >> gradle.properties

# Build the uber jar
RUN chmod +x ./gradlew && \
    ./gradlew :dist:jar -x test --no-daemon -q

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install Python3 for HTTP server
RUN apk add --no-cache python3

# Copy the built jar from builder stage to /data (not affected by volume mount)
COPY --from=builder /app/dist/build/libs/*.jar /data/target.jar

# Environment variables for Hadoop/Spark integration
ENV SPARK_USER=root
ENV JAVA_HOME=/opt/java/openjdk
ENV RUNTIME_JAVA_HOME=/opt/java/openjdk
ENV HADOOP_CONF_DIR=/etc/hadoop/conf
ENV SPARK_HOME=/opt/spark

# Create directories for Hadoop/Spark configuration
RUN mkdir -p ${HADOOP_CONF_DIR} && \
    mkdir -p /opt/spark && \
    mkdir -p /data

# Copy entrypoint script
COPY <<'EOF' /entrypoint.sh
#!/bin/sh
# If the mounted volume is empty, copy the built JAR to it for security scanning
if [ ! -s /app/target.jar ]; then
    echo "Volume is empty, copying built JAR for security scanning..."
    cp /data/target.jar /app/target.jar
fi
# Run a simple HTTP server on port 8080
cd /app && exec python3 -m http.server 8080
EOF
RUN chmod +x /entrypoint.sh

# Expose default port (library doesn't run a server, but container needs port for orchestration)
EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
CMD []