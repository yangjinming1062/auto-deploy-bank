# syntax=docker/dockerfile:1

# Stage 1: Build stage using Eclipse Temurin JDK 21 (Ubuntu-based for glibc compatibility)
FROM eclipse-temurin:21-jdk AS builder

# Install git and bash for build scripts
RUN apt-get update && apt-get install -y --no-install-recommends git bash && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /build

# Copy gradle configuration files first for better caching
COPY gradle.properties ./
COPY gradlew ./
COPY gradle/ ./gradle/
COPY build.gradle ./
COPY settings.gradle ./

# Copy project source
COPY . .

# Build the project (skip tests, checks, and javadoc for speed)
RUN chmod +x gradlew && \
    export JAVA_HOME=/opt/java/openjdk && \
    ./gradlew distTar -x test -x check -x checkLicense -x javadoc --no-daemon --warning-mode=none

# Extract and prepare the distribution
RUN tar -xzf build/distributions/besu-*.tar.gz -C build/distributions/

# Create target.jar for security scanning (combines all lib JARs)
RUN find build/distributions/besu-*/lib -name "*.jar" -type f | xargs -r jar cf build/distributions/target.jar

# Stage 2: Final runtime image using Eclipse Temurin JRE (glibc-compatible)
FROM eclipse-temurin:21-jre AS runtime

# Install additional dependencies
RUN apt-get update && apt-get install -y --no-install-recommends libjemalloc-dev=5.* && \
  apt-get clean && rm -rf /var/lib/apt/lists/* && \
  # Create besu user with UID 1000
  userdel ubuntu 2>/dev/null || true && rm -rf /home/ubuntu 2>/dev/null || true && \
  useradd --uid 1000 --create-home --home-dir /opt/besu --shell /bin/bash --user-group --skel /etc/skel besu && \
  chmod 0755 /opt/besu

# Copy the Besu distribution
COPY --from=builder /build/build/distributions/besu-* /opt/besu

# Copy target.jar for security scanning
COPY --from=builder /build/build/distributions/target.jar /opt/besu/target.jar

# Copy configuration files
COPY --chown=besu:besu config/ /opt/besu/config/

# Create data directory
RUN mkdir -p /opt/besu/data && chown -R besu:besu /opt/besu

# Set ownership
RUN chown -R besu:besu /opt/besu

USER ${BESU_USER:-besu}
WORKDIR /opt/besu

# Expose service ports
# 8545 HTTP JSON-RPC
# 8546 WS JSON-RPC
# 8547 HTTP GraphQL
# 8550 HTTP ENGINE JSON-RPC
# 8551 WS ENGINE JSON-RPC
# 30303 P2P
EXPOSE 8545 8546 8547 8550 8551 30303 9545

# Environment variables
ENV JAVA_HOME="/opt/java/openjdk"
ENV PATH="/opt/besu/bin:${JAVA_HOME}/bin:${PATH}"
ENV BESU_HOME="/opt/besu"
ENV BESU_RPC_HTTP_HOST="0.0.0.0"
ENV BESU_RPC_WS_HOST="0.0.0.0"
ENV BESU_GRAPHQL_HTTP_HOST="0.0.0.0"
ENV BESU_PID_PATH="/tmp/pid"

# Set BESU_OPTS for additional JVM options
ENV BESU_OPTS="-Dbesu.home=/opt/besu"

# Health check
HEALTHCHECK --start-period=30s --interval=10s --timeout=5s --retries=10 CMD bash -c "[ -f /tmp/pid ]" || exit 1

# Entry point - use the besu script
ENTRYPOINT ["bin/besu"]