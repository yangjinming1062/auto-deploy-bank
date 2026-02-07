#
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
# limitations under the License.

# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy pom.xml first for dependency caching
COPY pom.xml ./
RUN mvn dependency:go-offline -B -DskipTests || true

# Copy source code
COPY . .

# Build the project (skip tests for faster build)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

# Install bash for startup script
RUN apk add --no-cache bash

# Set environment variables
ENV AMORO_HOME=/opt/amoro
ENV AMORO_CONF_DIR=${AMORO_HOME}/conf
ENV AMORO_LOG_DIR=${AMORO_HOME}/logs
ENV JAVA_OPTS="-Xms512m -Xmx2048m"

# Create directories
RUN mkdir -p ${AMORO_HOME}/lib \
    ${AMORO_HOME}/conf \
    ${AMORO_HOME}/bin \
    ${AMORO_HOME}/logs \
    ${AMORO_HOME}/run

# Copy JRE-only runtime from builder
# Copy to /app/target.jar for security scanning AND to ${AMORO_HOME}/lib/amoro-ams.jar for runtime
COPY --from=builder /build/amoro-ams/target/amoro-ams-*.jar /app/target.jar
COPY --from=builder /build/amoro-ams/target/amoro-ams-*.jar ${AMORO_HOME}/lib/amoro-ams.jar

# Copy dependency jars
COPY --from=builder /build/amoro-ams/target/amoro-ams-dependency/lib/*.jar ${AMORO_HOME}/lib/

# Copy configuration files
COPY --from=builder /build/conf/config.yaml ${AMORO_CONF_DIR}/config.yaml
COPY --from=builder /build/conf/jvm.properties ${AMORO_CONF_DIR}/jvm.properties

# Copy log4j configuration
COPY --from=builder /build/amoro-ams/src/main/resources/log4j2.xml ${AMORO_CONF_DIR}/log4j2.xml

# Copy SQL initialization scripts (excluded from JAR by pom.xml)
COPY --from=builder /build/amoro-ams/src/main/resources/derby ${AMORO_CONF_DIR}/derby
COPY --from=builder /build/amoro-ams/src/main/resources/mysql ${AMORO_CONF_DIR}/mysql
COPY --from=builder /build/amoro-ams/src/main/resources/postgres ${AMORO_CONF_DIR}/postgres

# Create the startup script
RUN cat > ${AMORO_HOME}/bin/start.sh << 'SCRIPT'
#!/bin/bash
set -e

# Configure log level from environment
if [ -n "$LOG_LEVEL" ]; then
  export CONSOLE_LOG_LEVEL=$LOG_LEVEL
fi

# Read JVM options from jvm.properties file
JVM_OPTS_FROM_FILE=""
if [ -f "${AMORO_CONF_DIR}/jvm.properties" ]; then
  while IFS= read -r line || [ -n "$line" ]; do
    # Skip comments and empty lines
    [[ "$line" =~ ^#.*$ ]] && continue
    [[ -z "${line// }" ]] && continue
    JVM_OPTS_FROM_FILE="${JVM_OPTS_FROM_FILE} ${line}"
  done < "${AMORO_CONF_DIR}/jvm.properties"
fi

# Configure JVM options from environment variables (JVM_* -> -D*.*.*)
# e.g., JVM_XMX_CONFIG=2048 becomes -Dxm.x.config=2048
JVM_OPTS_FROM_ENV=""
for opt in $(printenv | grep "^JVM_" | sed 's/JVM_//' | sed 's/=.*//'); do
  key=$(echo "$opt" | tr '_' '.')
  value=$(printenv "JVM_$opt")
  JVM_OPTS_FROM_ENV="${JVM_OPTS_FROM_ENV} -D${key}=${value}"
done

# Build classpath
CLASSPATH=${AMORO_CONF_DIR}:${AMORO_HOME}/lib/amoro-ams.jar
for jar in ${AMORO_HOME}/lib/*.jar; do
  CLASSPATH="${CLASSPATH}:${jar}"
done

# Run the application with all JVM options
exec java \
  ${JAVA_OPTS} \
  ${JVM_OPTS_FROM_FILE} \
  ${JVM_OPTS_FROM_ENV} \
  -cp "${CLASSPATH}" \
  -Dlog4j.configurationFile=${AMORO_CONF_DIR}/log4j2.xml \
  -Dlog.home=${AMORO_LOG_DIR} \
  -Dlog.dir=${AMORO_LOG_DIR} \
  -Duser.dir=${AMORO_HOME} \
  org.apache.amoro.server.AmoroServiceContainer
SCRIPT
RUN chmod +x ${AMORO_HOME}/bin/start.sh

# Expose ports (HTTP server, Thrift table service, Thrift optimizing service)
EXPOSE 1630 1260 1261

# Set working directory
WORKDIR ${AMORO_HOME}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:1630/api/ams/v1/health/status || exit 1

# Set entrypoint
ENTRYPOINT ["/opt/amoro/bin/start.sh"]