#
# Copyright 2024 Apollo Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Multi-stage build for Apollo Assembly
# Stage 1: Builder - Compile and package the application
FROM maven:3.8.6-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy all project files
COPY pom.xml .
COPY apollo-assembly apollo-assembly
COPY apollo-common apollo-common
COPY apollo-biz apollo-biz
COPY apollo-configservice apollo-configservice
COPY apollo-adminservice apollo-adminservice
COPY apollo-portal apollo-portal
COPY apollo-audit apollo-audit
COPY apollo-build-sql-converter apollo-build-sql-converter
COPY apollo-buildtools apollo-buildtools
COPY scripts scripts

# Build the application (JAR will be copied out for security scanning)
RUN mvn clean package -DskipTests -B -pl apollo-assembly -am

# Stage 2: Runtime - JRE environment
FROM eclipse-temurin:17-jre-alpine

LABEL maintainer="Apollo Team <apollo-config@googlegroups.com>"
LABEL description="Apollo Configuration Management System - Assembly"

# Set environment variables
ENV APOLLO_RUN_MODE="Docker"
ENV JAVA_OPTS="-Xms256m -Xmx512m"

# Install curl for health checks
RUN apk add --no-cache curl tzdata && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone

# Create logs and app directories
RUN mkdir -p /opt/logs /app

# Copy the built JAR from builder stage
COPY --from=builder /app/apollo-assembly/target/*.jar app.jar

# Expose ports (configservice: 8080, adminservice: 8090, portal: 8070)
# Only the portal UI (8070) will be exposed externally via docker-compose
EXPOSE 8080 8090 8070

# Add volume for logs
VOLUME ["/opt/logs"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8070/health || exit 1

# Start the application
CMD ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]