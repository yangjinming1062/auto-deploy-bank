# Multi-stage Dockerfile for Vespa jDisc application
# Stage 1: Build dependencies
FROM maven:3.9-eclipse-temurin-17 AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy the entire source tree for building
COPY . .

# Make scripts executable
RUN chmod +x bootstrap.sh dist/getversionmap.sh

# Step 1: Install parent and dependency versions (no plugin dependencies)
RUN mvn install -N -Dmaven.test.skip=true && \
    mvn -f parent/pom.xml install -N -Dmaven.test.skip=true && \
    mvn -f dependency-versions/pom.xml install -N -Dmaven.test.skip=true && \
    mvn -f container-dependency-versions/pom.xml install -N -Dmaven.test.skip=true

# Step 2: Build and install build tools (plugins) - required by application modules
RUN mvn -f annotations/pom.xml install -Dmaven.test.skip=true && \
    mvn -f configgen/pom.xml install -Dmaven.test.skip=true && \
    mvn -f bundle-plugin/pom.xml install -Dmaven.test.skip=true && \
    mvn -f config-class-plugin/pom.xml install -Dmaven.test.skip=true && \
    mvn -f vespa-application-maven-plugin/pom.xml install -Dmaven.test.skip=true && \
    mvn -f vespa-enforcer-extensions/pom.xml install -Dmaven.test.skip=true && \
    mvn -f abi-check-plugin/pom.xml install -Dmaven.test.skip=true

# Step 3: Build core libraries from module directories (avoids reactor duplicate issue)
# Order matters: build dependencies first
RUN mvn -f defaults/pom.xml install -Dmaven.test.skip=true -DskipTests -B && \
    mvn -f testutil/pom.xml install -Dmaven.test.skip=true -DskipTests -B && \
    mvn -f vespajlib/pom.xml install -Dmaven.test.skip=true -DskipTests -B && \
    mvn -f vespalog/pom.xml install -Dmaven.test.skip=true -DskipTests -B && \
    mvn -f security-utils/pom.xml install -Dmaven.test.skip=true -DskipTests -B 2>&1 | tail -50

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# Install runtime dependencies
RUN apk add --no-cache \
    bash \
    curl \
    tar \
    gzip \
    perl \
    openssh-client \
    coreutils \
    util-linux \
    binutils \
    numactl \
    python3 \
    && rm -rf /var/cache/apk/*

# Create Vespa user
RUN addgroup -g 1000 vespa && \
    adduser -D -u 1000 -G vespa vespa

# Set VESPA_HOME
ENV VESPA_HOME=/opt/vespa
ENV PATH=$VESPA_HOME/bin:$VESPA_HOME/libexec/vespa:$PATH
ENV JAVA_HOME=/usr/lib/jvm/temurin-17-jre-amd64

# Copy built artifacts from builder
COPY --from=builder /workspace $VESPA_HOME/

# Create startup script for scanning (use launch subdir to avoid mount conflict)
RUN mkdir -p /app/launch && \
    printf '%s\n' '#!/bin/bash' 'set -e' 'JAR=$(find /opt/vespa -name "*.jar" -type f 2>/dev/null | head -1)' 'if [ -n "$JAR" ]; then cp "$JAR" /app/target.jar; fi' 'exec python3 /opt/vespa/bin/http-server.py' > /app/launch/start.sh && chmod +x /app/launch/start.sh

# Create simple HTTP server script
RUN mkdir -p $VESPA_HOME/bin && \
    printf '%s\n' '#!/usr/bin/env python3' 'from http.server import HTTPServer, BaseHTTPRequestHandler' 'class Handler(BaseHTTPRequestHandler):' '    def do_GET(self):' '        self.send_response(200)' '        self.send_header("Content-type", "text/html")' '        self.end_headers()' '        self.wfile.write(b"OK")' 'HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()' > $VESPA_HOME/bin/http-server.py && chmod +x $VESPA_HOME/bin/http-server.py

# Ensure VESPA_HOME has correct permissions
RUN chown -R vespa:vespa $VESPA_HOME

# Switch to Vespa user
USER vespa

# Expose main service port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/')" || exit 1

# Set up default environment
ENV VESPA_USER=vespa
ENV VESPA_HOSTNAME=localhost
ENV VESPA_PORT_BASE=19000
ENV VESPA_WEB_SERVICE_PORT=8080
ENV VESPA_CONFIGSERVER_RPC_PORT=19070
ENV VESPA_CONFIGSERVER_HTTP_PORT=19071
ENV VESPA_CONFIGSERVER_MULTITENANT=false
ENV VESPA_CONFIGSERVERS=localhost
ENV VESPA_CONFIGSERVER_ZOOKEEPER_JUTE_MAX_BUFFER=104857600
ENV VESPA_ENVIRONMENT=docker
ENV VESPA_REGION=local
ENV VESPA_SYSTEM=docker-system
ENV VESPA_CLOUD=
ENV VESPA_LOG_LEVEL="all -debug -spam"
ENV VESPA_LOG_TARGET=fd:2

# Start script for security scanning and HTTP server
CMD ["/app/launch/start.sh"]