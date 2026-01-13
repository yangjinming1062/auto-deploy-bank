#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

# Multi-stage build for Gravitino server
# Stage 1: Build stage with Gradle wrapper
FROM gradle:8.5-jdk17 AS builder

# Set working directory
WORKDIR /build

# Copy Gradle configuration
COPY settings.gradle.kts .
COPY build.gradle.kts .
COPY gradle.properties .

# Copy source code
COPY . .

# Build the distribution (excluding tests and RAT license check)
# Note: Using gradle directly instead of gradlew to avoid permission issues
# Skipping RAT check because Dockerfile and docker-compose.yaml are being added
# Running compileDistribution to create the distribution package
RUN gradle compileDistribution -x rat -x test --no-daemon && \
    ls -la /build/distribution/package/bin/ | head -10

# Stage 2: Runtime stage with JRE only
FROM eclipse-temurin:17-jre-jammy

# Set labels
LABEL maintainer="dev@gravitino.apache.org"

# Create working directory
WORKDIR /app

# Set environment variables
ENV GRAVITINO_HOME=/app
ENV GRAVITINO_CONF_DIR=/app/conf
ENV GRAVITINO_LOG_DIR=/app/logs
ENV JAVA_OPTS="-Xms1024m -Xmx1024m -XX:MaxMetaspaceSize=512m"

# Install python for scripts
RUN apt-get update && apt-get install -y \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Copy built distribution from builder
COPY --from=builder /build/distribution/package /app

# Create logs directory
RUN mkdir -p /app/logs

# Copy the create-user script and make it executable
COPY create-user.sh /app/create-user.sh
RUN chmod +x /app/create-user.sh

# Copy and set entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Set proper permissions
RUN chmod +x /app/bin/gravitino.sh

# Set entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]

# Expose ports (main server, iceberg-rest, lance-rest)
EXPOSE 8090 9001 9101

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8090/api/version || exit 1