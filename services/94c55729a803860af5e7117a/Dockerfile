#
# Copyright (c) 2024 Oracle and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Multi-stage build for Helidon LRA Coordinator Server

# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /build

# Copy entire project structure (excluding .dockerignore patterns)
COPY . .

# Build only the LRA coordinator server module and its dependencies
RUN mvn clean package -DskipTests -B -pl :helidon-lra-coordinator-server -am

# Stage 2: Runtime image
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Create directory for JAR extraction
RUN mkdir -p /app/jars-extracted

# Copy JAR and dependencies from builder stage
COPY --from=builder /build/lra/coordinator/server/target/helidon-lra-coordinator-server.jar /app/app.jar
COPY --from=builder /build/lra/coordinator/server/target/helidon-lra-coordinator-server.jar /app/target.jar
COPY --from=builder /build/lra/coordinator/server/target/helidon-lra-coordinator-server.jar /app/jars-extracted/target.jar
COPY --from=builder /build/lra/coordinator/server/target/libs /app/libs

# Copy configuration files
COPY --from=builder /build/lra/coordinator/server/src/main/resources/application.yaml /app/
COPY --from=builder /build/lra/coordinator/server/src/main/resources/logging.properties /app/

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Install curl for health checks
RUN apk add --no-cache curl

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8070/health || exit 1

# Expose port
EXPOSE 8070

# Run the application
CMD ["java", "-jar", "/app/app.jar"]
