# Multi-stage build for OpenRewrite
# Stage 1: Build stage with all dependencies
FROM eclipse-temurin:21-jdk as builder

# Set working directory
WORKDIR /app

# Install dependencies for building
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install multiple JDK versions for different modules
RUN apt-get update && apt-get install -y \
    openjdk-8-jdk \
    openjdk-11-jdk \
    openjdk-17-jdk \
    openjdk-25-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set Java 17 as default for Gradle (Gradle 9.x requires Java 17+)
# Modules can override this for their specific needs
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Node.js for TypeScript compilation
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest

# Copy all source code
COPY . .

# Make gradlew executable
RUN chmod +x gradlew

# Build only the required modules for the RPC server (skip tests for faster build)
RUN ./gradlew :rewrite-core:build :rewrite-java:build :rewrite-json:build :rewrite-javascript:build -x test --no-daemon

# Build TypeScript components
RUN cd rewrite-javascript/rewrite && \
    npm ci && \
    npm run build

# Create a single bundled JAR for security scanning
RUN rm -rf /app/target.jar && \
    mkdir -p /tmp/jar-bundle && \
    find /app -name "*.jar" -path "*/build/libs/*" -exec cp {} /tmp/jar-bundle/ \; && \
    cd /tmp/jar-bundle && \
    jar -cvf target.jar *.jar && \
    mv target.jar /app/ && \
    rm -rf /tmp/jar-bundle

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

# Install Node.js for running the RPC server
RUN apk add --no-cache nodejs npm

# Set working directory
WORKDIR /app

# Copy built JARs from builder stage
COPY --from=builder /app/rewrite-javascript/build/libs/*.jar /app/
COPY --from=builder /app/rewrite-core/build/libs/*.jar /app/
COPY --from=builder /app/rewrite-java/build/libs/*.jar /app/
COPY --from=builder /app/rewrite-json/build/libs/*.jar /app/

# Copy bundled JAR for security scanning
COPY --from=builder /app/target.jar /app/target.jar

# Copy built TypeScript dist
COPY --from=builder /app/rewrite-javascript/rewrite/dist /app/dist

# Copy TypeScript source for the RPC server
COPY --from=builder /app/rewrite-javascript/rewrite/node_modules /app/node_modules

# Copy HTTP proxy
COPY http-proxy.js /app/http-proxy.js
RUN chmod +x /app/http-proxy.js

# Install wget for healthcheck
RUN apk add --no-cache wget

# Create script to start the HTTP proxy which wraps the RPC server
RUN echo '#!/bin/sh' > /app/start-server.sh && \
    echo 'exec node /app/http-proxy.js' >> /app/start-server.sh && \
    chmod +x /app/start-server.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ || exit 1

# Set the entrypoint to the start script
ENTRYPOINT ["/app/start-server.sh"]

# Default command (will be overridden by docker-compose)
CMD []