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

# Stage 1: Build the application with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy Maven configuration files and source code
COPY pom.xml .
COPY application/pom.xml application/
COPY application/src application/src
COPY common/pom.xml common/
COPY common/data common/data
COPY common/proto common/proto
COPY common/util common/util
COPY common/message common/message
COPY common/actor common/actor
COPY common/queue common/queue
COPY common/transport common/transport
COPY common/dao-api common/dao-api
COPY common/cluster-api common/cluster-api
COPY common/stats common/stats
COPY common/cache common/cache
COPY common/coap-server common/coap-server
COPY common/edge-api common/edge-api
COPY common/version-control common/version-control
COPY common/script common/script
COPY common/edqs common/edqs
COPY common/discovery-api common/discovery-api
COPY rule-engine/pom.xml rule-engine/
COPY rule-engine/rule-engine-api rule-engine/rule-engine-api
COPY rule-engine/rule-engine-components rule-engine/rule-engine-components
COPY dao/pom.xml dao/
COPY dao dao
COPY edqs/pom.xml edqs/
COPY edqs edqs
COPY transport/pom.xml transport/
COPY transport/http transport/http
COPY transport/mqtt transport/mqtt
COPY transport/coap transport/coap
COPY transport/lwm2m transport/lwm2m
COPY transport/snmp transport/snmp
COPY ui-ngx/pom.xml ui-ngx/
COPY ui-ngx/src ui-ngx/src
COPY tools/pom.xml tools/
COPY tools tools
COPY rest-client/pom.xml rest-client/
COPY rest-client rest-client
COPY monitoring/pom.xml monitoring/
COPY monitoring monitoring
COPY netty-mqtt/pom.xml netty-mqtt/
COPY netty-mqtt netty-mqtt
COPY msa/pom.xml msa/
COPY msa/tb msa/tb
COPY msa/web-ui msa/web-ui
COPY msa/vc-executor msa/vc-executor
COPY msa/vc-executor-docker msa/vc-executor-docker
COPY msa/tb-node msa/tb-node
COPY msa/transport msa/transport
COPY msa/js-executor msa/js-executor
COPY msa/monitoring msa/monitoring
COPY msa/edqs msa/edqs
COPY msa/black-box-tests msa/black-box-tests
COPY packaging packaging
COPY .git .git
COPY lombok.config .
COPY license-header-template.txt .

# Download dependencies and build the application (skip frontend yarn build for faster container build)
# Skip git-commit-id plugin by setting failOnNoGitDirectories to false
RUN mvn clean package -DskipTests -B -P-yarn-build -Dmaven.gitcommitid.skip=true && \
    ls -la application/target/

# Stage 2: Create runtime image
FROM eclipse-temurin:17-jre-alpine

# Install PostgreSQL client and netcat for health checks
RUN apk add --no-cache postgresql-client netcat-openbsd

WORKDIR /app

# Copy the JAR file from builder stage (use boot.jar for executable Spring Boot JAR)
COPY --from=builder /build/application/target/thingsboard-4.3.0-SNAPSHOT-boot.jar app.jar

# Also copy to target.jar location for security scanning volume mount
RUN cp app.jar target.jar

# Copy SQL schema files for database initialization (to data directory for install service)
COPY --from=builder /build/dao/src/main/resources/sql/ /app/data/sql/

# Create entrypoint script for database initialization
RUN printf '%s\n' '#!/bin/bash' \
'# Wait for database to be ready' \
'echo "Waiting for PostgreSQL to be ready..."' \
'until pg_isready -h postgres -p 5432; do' \
'  echo "PostgreSQL is unavailable - sleeping"' \
'  sleep 1' \
'done' \
'echo "PostgreSQL is ready!"' \
'' \
'# Check if database is already initialized' \
'if psql -h postgres -U postgres -d thingsboard -c "\dt" 2>/dev/null | grep -q "admin_settings"; then' \
'  echo "Database already initialized, starting ThingsBoard..."' \
'else' \
'  echo "Initializing database..."' \
'  java -cp /app/app.jar \' \
'    -Dloader.main=org.thingsboard.server.ThingsboardInstallApplication \' \
'    -Dinstall.data_dir=/app/data \' \
'    -Dinstall.load_demo=false \' \
'    -Dspring.jpa.hibernate.ddl-auto=none \' \
'    -Dinstall.upgrade=false \' \
'    -Dspring.datasource.url=jdbc:postgresql://postgres:5432/thingsboard \' \
'    -Dspring.datasource.username=postgres \' \
'    -Dspring.datasource.password=postgres \' \
'    -Dspring.datasource.driver-class-name=org.postgresql.Driver \' \
'    org.springframework.boot.loader.launch.PropertiesLauncher' \
'  echo "Database initialization complete!"' \
'fi' \
'' \
'# Start ThingsBoard' \
'exec java -jar /app/app.jar' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Expose HTTP port
EXPOSE 8080

# Create a non-root user (Alpine Linux)
RUN addgroup -S -g 1001 thingsboard && \
    adduser -S -D -u 1001 -G thingsboard thingsboard

# Create data directory
RUN mkdir -p /app/data && chown -R thingsboard:thingsboard /app

# Change to non-root user
USER thingsboard

# Health check - use TCP check since all HTTP endpoints require authentication
HEALTHCHECK --interval=30s --timeout=3s --start-period=120s --retries=5 \
    CMD nc -z localhost 8080 || exit 1

# Entrypoint script runs database install if needed, then starts the application
ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]