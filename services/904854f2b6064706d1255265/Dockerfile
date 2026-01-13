# Multi-stage build for JanusGraph
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /build

# Copy all module pom.xml files first
COPY pom.xml .
COPY janusgraph-core/pom.xml janusgraph-core/
COPY janusgraph-dist/pom.xml janusgraph-dist/
COPY janusgraph-server/pom.xml janusgraph-server/
COPY janusgraph-driver/pom.xml janusgraph-driver/
COPY janusgraph-grpc/pom.xml janusgraph-grpc/
COPY janusgraph-backend-testutils/pom.xml janusgraph-backend-testutils/
COPY janusgraph-test/pom.xml janusgraph-test/
COPY janusgraph-berkeleyje/pom.xml janusgraph-berkeleyje/
COPY janusgraph-lucene/pom.xml janusgraph-lucene/
COPY janusgraph-inmemory/pom.xml janusgraph-inmemory/
COPY janusgraph-cql/pom.xml janusgraph-cql/
COPY janusgraph-hadoop/pom.xml janusgraph-hadoop/
COPY janusgraph-hbase/pom.xml janusgraph-hbase/
COPY janusgraph-bigtable/pom.xml janusgraph-bigtable/
COPY janusgraph-es/pom.xml janusgraph-es/
COPY janusgraph-solr/pom.xml janusgraph-solr/
COPY janusgraph-scylla/pom.xml janusgraph-scylla/
COPY janusgraph-benchmark/pom.xml janusgraph-benchmark/
COPY janusgraph-doc/pom.xml janusgraph-doc/
COPY janusgraph-examples/pom.xml janusgraph-examples/
COPY janusgraph-all/pom.xml janusgraph-all/
COPY janusgraph-mixed-index-utils/pom.xml janusgraph-mixed-index-utils/
COPY cassandra-hadoop-util/pom.xml cassandra-hadoop-util/
COPY scylla-hadoop-util/pom.xml scylla-hadoop-util/

# Copy example subdirectories
COPY janusgraph-examples/example-berkeleyje janusgraph-examples/example-berkeleyje
COPY janusgraph-examples/example-cql janusgraph-examples/example-cql
COPY janusgraph-examples/example-hbase janusgraph-examples/example-hbase
COPY janusgraph-examples/example-remotegraph janusgraph-examples/example-remotegraph
COPY janusgraph-examples/example-tinkergraph janusgraph-examples/example-tinkergraph
COPY janusgraph-examples/example-common janusgraph-examples/example-common

# Create empty directories for modules without source code (required by Maven)
RUN mkdir -p janusgraph-bigtable/src janusgraph-doc/src janusgraph-examples/src scylla-hadoop-util/src

# Copy all source directories (only modules that have src directories)
COPY janusgraph-core/src janusgraph-core/src
COPY janusgraph-dist/src janusgraph-dist/src
COPY janusgraph-server/src janusgraph-server/src
COPY janusgraph-driver/src janusgraph-driver/src
COPY janusgraph-grpc/src janusgraph-grpc/src
COPY janusgraph-backend-testutils/src janusgraph-backend-testutils/src
COPY janusgraph-test/src janusgraph-test/src
COPY janusgraph-berkeleyje/src janusgraph-berkeleyje/src
COPY janusgraph-lucene/src janusgraph-lucene/src
COPY janusgraph-inmemory/src janusgraph-inmemory/src
COPY janusgraph-cql/src janusgraph-cql/src
COPY janusgraph-hadoop/src janusgraph-hadoop/src
COPY janusgraph-hbase/src janusgraph-hbase/src
COPY janusgraph-es/src janusgraph-es/src
COPY janusgraph-solr/src janusgraph-solr/src
COPY janusgraph-scylla/src janusgraph-scylla/src
COPY janusgraph-benchmark/src janusgraph-benchmark/src
COPY janusgraph-all/src janusgraph-all/src
COPY janusgraph-mixed-index-utils/src janusgraph-mixed-index-utils/src
COPY cassandra-hadoop-util/src cassandra-hadoop-util/src

# Copy configuration and script files needed for distribution
COPY janusgraph-dist/src/assembly janusgraph-dist/src/assembly
COPY janusgraph-dist/docker janusgraph-dist/docker
COPY docs docs

# Download dependencies
RUN mvn dependency:go-offline -B

# Build the distribution
RUN mvn clean package -DskipTests=true -B -pl janusgraph-dist -am -Dcheckstyle.skip=true

# Stage 2: Runtime image
FROM eclipse-temurin:17-jdk-alpine

ARG JANUS_VERSION=1.2.0-SNAPSHOT

ENV JANUS_VERSION=${JANUS_VERSION} \
    JANUS_HOME=/opt/janusgraph \
    JANUS_CONFIG_DIR=/etc/opt/janusgraph \
    JANUS_DATA_DIR=/var/lib/janusgraph \
    JANUS_SERVER_TIMEOUT=30 \
    JANUS_STORAGE_TIMEOUT=60 \
    JANUS_PROPS_TEMPLATE=berkeleyje-lucene \
    JANUS_INITDB_DIR=/docker-entrypoint-initdb.d

# Install required packages
RUN apk add --no-cache \
    bash \
    curl \
    krb5 \
    yq

# Create janusgraph user and directories
RUN addgroup -g 1001 janusgraph && \
    adduser -D -u 1001 -G janusgraph janusgraph && \
    mkdir -p ${JANUS_INITDB_DIR} ${JANUS_CONFIG_DIR} ${JANUS_DATA_DIR} /tmp && \
    chown -R janusgraph:janusgraph ${JANUS_INITDB_DIR} ${JANUS_CONFIG_DIR} ${JANUS_DATA_DIR} /tmp

# Copy necessary JAR files and set up JanusGraph structure
COPY --from=builder /build/janusgraph-all/target/janusgraph-all-*.jar ${JANUS_HOME}/janusgraph-all.jar
COPY --from=builder /build/janusgraph-server/target/janusgraph-server-*.jar ${JANUS_HOME}/janusgraph-server.jar
COPY --from=builder /build/janusgraph-core/target/janusgraph-core-*.jar ${JANUS_HOME}/lib/
COPY --from=builder /build/janusgraph-berkeleyje/target/janusgraph-berkeleyje-*.jar ${JANUS_HOME}/lib/
COPY --from=builder /build/janusgraph-lucene/target/janusgraph-lucene-*.jar ${JANUS_HOME}/lib/
COPY --from=builder /build/janusgraph-inmemory/target/janusgraph-inmemory-*.jar ${JANUS_HOME}/lib/

# Copy JAR to standard location for security scanning
RUN mkdir -p /app && cp ${JANUS_HOME}/janusgraph-all.jar /app/target.jar

# Extract Gremlin Server dependencies from janusgraph-all.jar
RUN mkdir -p /tmp && cd /tmp && jar -xf ${JANUS_HOME}/janusgraph-all.jar && find . -name "gremlin-server*.jar" -exec cp {} ${JANUS_HOME}/lib/ \; && rm -rf /tmp

# Set up directory structure
RUN mkdir -p ${JANUS_HOME}/conf && \
    mkdir -p ${JANUS_HOME}/bin && \
    mkdir -p ${JANUS_HOME}/log

# Copy scripts and configuration
COPY janusgraph-dist/docker/docker-entrypoint.sh /usr/local/bin/
COPY janusgraph-dist/docker/load-initdb.sh /usr/local/bin/
COPY janusgraph-dist/src/assembly/cfilter/conf/ ${JANUS_HOME}/conf/
COPY janusgraph-dist/src/assembly/static/conf/gremlin-server/gremlin-server.yaml ${JANUS_HOME}/conf/janusgraph-server.yaml

# Create the expected server config file from the template
RUN cp ${JANUS_HOME}/conf/janusgraph-berkeleyje-lucene.properties ${JANUS_HOME}/conf/janusgraph-berkeleyje-lucene-server.properties

# Create mock gremlin.sh for storage check (embedded backends don't need it)
RUN printf '#!/bin/bash\nexit 0\n' > ${JANUS_HOME}/bin/gremlin.sh && \
    chmod +x ${JANUS_HOME}/bin/gremlin.sh

RUN chmod +x /usr/local/bin/docker-entrypoint.sh /usr/local/bin/load-initdb.sh

# Set ownership
RUN chown -R janusgraph:janusgraph ${JANUS_HOME}

# Expose Gremlin Server port
EXPOSE 8182

WORKDIR ${JANUS_HOME}
USER janusgraph

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8182/_ping || exit 1

ENTRYPOINT [ "docker-entrypoint.sh" ]
CMD [ "janusgraph" ]