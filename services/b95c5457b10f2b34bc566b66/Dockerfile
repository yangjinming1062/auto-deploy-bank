# Stage 1: Build the plugin with Maven (using Java 8 for compatibility with groovy-eclipse-compiler)
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the plugin (skip tests for faster build)
RUN mvn clean package -DskipTests -B

# Copy all required dependencies
RUN mvn dependency:copy-dependencies -DoutputDirectory=/app/target/dependency -DincludeScope=runtime -B

# Stage 2: Runtime stage with Elasticsearch and the plugin (glibc-based for compatibility)
FROM eclipse-temurin:8-jre

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set ES version and download
ENV ES_VERSION=1.7.3
ENV ES_HOME=/elasticsearch

# Download and extract Elasticsearch
RUN curl -L -o /tmp/elasticsearch-${ES_VERSION}.tar.gz \
    https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-${ES_VERSION}.tar.gz && \
    tar -xzf /tmp/elasticsearch-${ES_VERSION}.tar.gz -C /opt && \
    mv /opt/elasticsearch-${ES_VERSION} ${ES_HOME} && \
    rm /tmp/elasticsearch-${ES_VERSION}.tar.gz

# Create plugin directory
RUN mkdir -p ${ES_HOME}/plugins/mongodb-river/lib

# Copy the built plugin JAR from builder stage
COPY --from=builder /app/target/elasticsearch-river-mongodb-2.0.12-SNAPSHOT.jar ${ES_HOME}/plugins/mongodb-river/lib/

# Copy all required dependencies (guava, mongo driver, etc.)
COPY --from=builder /app/target/dependency/*.jar ${ES_HOME}/plugins/mongodb-river/lib/

# Copy plugin descriptor
COPY --from=builder /app/target/classes/es-plugin.properties ${ES_HOME}/plugins/mongodb-river/

# Copy JAR backup for security scanning volume mount
COPY --from=builder /app/target/elasticsearch-river-mongodb-2.0.12-SNAPSHOT.jar ${ES_HOME}/plugins/mongodb-river/lib/elasticsearch-river-mongodb-2.0.12-SNAPSHOT.jar.bak

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set environment variables
ENV ES_HOME=/elasticsearch
ENV PATH=${ES_HOME}/bin:$PATH

# Configure Elasticsearch - disable mmap for better compatibility
RUN echo "network.host: 0.0.0.0" >> ${ES_HOME}/config/elasticsearch.yml && \
    echo "http.cors.enabled: true" >> ${ES_HOME}/config/elasticsearch.yml && \
    echo "http.cors.allow-origin: \"*\"" >> ${ES_HOME}/config/elasticsearch.yml && \
    echo "index.store.type: fs" >> ${ES_HOME}/config/elasticsearch.yml

# Patch elasticsearch script to add GC options for old ES compatibility
RUN sed -i 's/ES_JAVA_OPTS="/ES_JAVA_OPTS="-XX:+UseSerialGC -XX:-UseAdaptiveSizePolicy /g' ${ES_HOME}/bin/elasticsearch

# Expose Elasticsearch HTTP port
EXPOSE 9200

# Healthcheck for Elasticsearch
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=5 \
    CMD curl -f http://localhost:9200/ || exit 1

# Run Elasticsearch in foreground using entrypoint script
ENTRYPOINT ["/entrypoint.sh"]