# Multi-stage build for Apache Solr from source
# Stage 1: Build Solr from source using Gradle
FROM eclipse-temurin:21-jdk AS builder

# Set working directory
WORKDIR /build

# Copy Gradle wrapper and build files
COPY . .

# Make gradlew executable
RUN chmod +x gradlew

# Build Solr distribution (this will take several minutes)
# The 'dev' task creates a development distribution with all modules
RUN ./gradlew dev --no-daemon

# Stage 2: Runtime image
FROM eclipse-temurin:21-jre-alpine

# Install required runtime dependencies
RUN apk add --no-cache bash curl procps

# Set environment variables
ENV SOLR_USER="solr" \
    SOLR_UID="8983" \
    SOLR_GROUP="solr" \
    SOLR_GID="8983" \
    PATH="/opt/solr/bin:$PATH" \
    SOLR_INCLUDE=/etc/default/solr.in.sh \
    SOLR_HOME="/var/solr/data" \
    SOLR_PID_DIR="/var/solr" \
    SOLR_LOGS_DIR="/var/solr/logs" \
    LOG4J_PROPS="/var/solr/log4j2.xml" \
    SOLR_HOST_BIND="0.0.0.0" \
    SOLR_ZOOKEEPER_EMBEDDED_HOST="0.0.0.0" \
    SOLR_PORT="8983"

# Create solr user and group
RUN addgroup -g 8983 solr && \
    adduser -u 8983 -G solr -s /bin/bash -D solr

# Copy the built Solr distribution from builder stage
COPY --from=builder /build/solr/packaging/build/dev /opt/solr

# Set up Solr directories and permissions
RUN mkdir -p -m 0770 /var/solr/data && \
    chown -R solr:solr /var/solr /opt/solr && \
    mkdir -p /opt/solr/server/solr/lib

# Copy configuration files
COPY solr/server/solr/solr.xml /opt/solr/server/solr/solr.xml
COPY solr/server/resources/log4j2.xml /var/solr/log4j2.xml

# Expose Solr port
EXPOSE 8983

# Switch to solr user
USER solr

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8983/solr/admin/cores || exit 1

# Start Solr in foreground mode
CMD ["/opt/solr/bin/solr", "start", "-f"]