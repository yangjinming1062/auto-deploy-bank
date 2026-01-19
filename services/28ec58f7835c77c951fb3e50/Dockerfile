#
# Copyright © 2016-2025 The Thingsboard Authors
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

# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy all project files (multi-module project requires all modules)
COPY . .

# Build the application (skip git plugin if .git directory is not available, format licenses first)
RUN mvn -B license:format -DskipTests && \
    mvn -B clean package -DskipTests -Dmaven.gitcommitid.skip=true -pl application -am

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# Install curl for healthcheck and postgresql-client for install checks
RUN apk add --no-cache curl postgresql-client

WORKDIR /app

# Copy the built JAR from builder stage (use the Spring Boot executable JAR)
COPY --from=builder /build/application/target/thingsboard-*-boot.jar /app/target.jar

# Copy SQL schema files for installation
COPY --from=builder /build/dao/target/classes/sql /app/sql

# Create non-root user (handle existing UID/GID in Alpine)
RUN addgroup -S thingsboard 2>/dev/null || true && \
    adduser -S -u 1000 -G thingsboard thingsboard 2>/dev/null || true && \
    chown -R thingsboard:thingsboard /app
USER thingsboard

# Expose the internal port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/api/version || exit 1

# Start the application
CMD ["java", "-jar", "target.jar"]