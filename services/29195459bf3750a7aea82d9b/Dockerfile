# Multi-stage Dockerfile for Apache NiFi
# Build stage
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /build

# Copy Maven wrapper and pom.xml
COPY .mvn .mvn
COPY mvnw pom.xml ./

# Copy all source code
COPY . .

# Make Maven wrapper executable
WORKDIR /build
RUN chmod +x ./mvnw

# Build NiFi assembly (with all dependencies)
RUN ./mvnw install -T1C -am -pl :nifi-assembly -DskipTests -B

# Runtime stage
FROM eclipse-temurin:21-jre-alpine

ARG MAINTAINER="Apache NiFi <dev@nifi.apache.org>"
LABEL maintainer="${MAINTAINER}"
LABEL site="https://nifi.apache.org"

ARG UID=1000
ARG GID=1000

ENV NIFI_BASE_DIR=/opt/nifi
ENV NIFI_HOME=${NIFI_BASE_DIR}/nifi-current
ENV NIFI_TOOLKIT_HOME=${NIFI_BASE_DIR}/nifi-toolkit-current
ENV NIFI_PID_DIR=${NIFI_HOME}/run
ENV NIFI_LOG_DIR=${NIFI_HOME}/logs

# Install necessary packages
RUN apk add --no-cache \
    bash \
    curl \
    procps \
    unzip \
    xmlstarlet \
    jq

# Setup NiFi user and create necessary directories
RUN addgroup -g ${GID} nifi || true \
    && adduser -D -u ${UID} -G nifi -s /bin/bash nifi \
    && mkdir -p ${NIFI_BASE_DIR} \
    && mkdir -p ${NIFI_HOME}/conf \
    && mkdir -p ${NIFI_HOME}/database_repository \
    && mkdir -p ${NIFI_HOME}/flowfile_repository \
    && mkdir -p ${NIFI_HOME}/content_repository \
    && mkdir -p ${NIFI_HOME}/provenance_repository \
    && mkdir -p ${NIFI_HOME}/python_extensions \
    && mkdir -p ${NIFI_HOME}/nar_extensions \
    && mkdir -p ${NIFI_HOME}/state \
    && mkdir -p ${NIFI_LOG_DIR} \
    && mkdir -p /app \
    && chown -R nifi:nifi ${NIFI_BASE_DIR} \
    && chown -R nifi:nifi /app

# Copy built NiFi from builder stage
COPY --from=builder /build/nifi-assembly/target/nifi-2.7.0-SNAPSHOT-bin.zip ${NIFI_BASE_DIR}/
RUN unzip -q ${NIFI_BASE_DIR}/nifi-2.7.0-SNAPSHOT-bin.zip -d ${NIFI_BASE_DIR}/tmp \
    && rm ${NIFI_BASE_DIR}/nifi-2.7.0-SNAPSHOT-bin.zip \
    && mv ${NIFI_BASE_DIR}/tmp/nifi-2.7.0-SNAPSHOT/* ${NIFI_HOME}/ \
    && mv ${NIFI_BASE_DIR}/tmp/nifi-2.7.0-SNAPSHOT/.* ${NIFI_HOME}/ 2>/dev/null || true \
    && rm -rf ${NIFI_BASE_DIR}/tmp \
    && ln -s ${NIFI_HOME} ${NIFI_BASE_DIR}/nifi-2.7.0-SNAPSHOT \
    && chown -R nifi:nifi ${NIFI_HOME}

# Clear nifi-env.sh in favour of configuring all environment variables in the Dockerfile
RUN echo "#!/bin/sh\n" > ${NIFI_HOME}/bin/nifi-env.sh 2>/dev/null || true && \
    chown nifi:nifi ${NIFI_HOME}/bin/nifi-env.sh 2>/dev/null || true

# Configure NiFi to listen on all interfaces via HTTP
RUN sed -i 's|^nifi.web.https.host=.*|#nifi.web.https.host=0.0.0.0|' ${NIFI_HOME}/conf/nifi.properties 2>/dev/null || true && \
    sed -i 's|^nifi.web.http.host=.*|nifi.web.http.host=0.0.0.0|' ${NIFI_HOME}/conf/nifi.properties 2>/dev/null || true && \
    sed -i 's|^nifi.web.http.port=.*|nifi.web.http.port=8080|' ${NIFI_HOME}/conf/nifi.properties 2>/dev/null || true && \
    printf '#!/bin/sh\nsed -i "s|^nifi.web.https.host=.*|#nifi.web.https.host=0.0.0.0|" /opt/nifi/nifi-current/conf/nifi.properties\nexec bin/nifi.sh run\n' > ${NIFI_HOME}/start.sh && \
    chmod +x ${NIFI_HOME}/start.sh

USER nifi

# Expose web UI, site-to-site, and jetty monitoring ports
EXPOSE 8080/tcp 10000/tcp 8000/tcp

WORKDIR ${NIFI_HOME}

# Volume mounts for persistence
VOLUME ${NIFI_LOG_DIR} \
       ${NIFI_HOME}/conf \
       ${NIFI_HOME}/database_repository \
       ${NIFI_HOME}/flowfile_repository \
       ${NIFI_HOME}/content_repository \
       ${NIFI_HOME}/provenance_repository \
       ${NIFI_HOME}/python_extensions \
       ${NIFI_HOME}/nar_extensions \
       ${NIFI_HOME}/state

# Start NiFi in foreground mode (required for Docker)
ENTRYPOINT ["bin/nifi.sh", "run"]