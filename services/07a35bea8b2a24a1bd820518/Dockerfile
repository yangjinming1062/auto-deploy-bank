################################################################################
# Stage 1: Builder - Build Elasticsearch from source
################################################################################
FROM eclipse-temurin:17-jdk AS builder

# Install required dependencies for building
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    zip \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /build

# Copy Gradle wrapper and build files
COPY gradlew .
COPY gradle.properties .
COPY settings.gradle .
COPY build.gradle .
COPY muted-tests.yml .
COPY renovate.json .
COPY .editorconfig .
COPY .gitattributes .
COPY .git-blame-ignore-revs .
COPY .dir-locals.el .

# Copy entire source tree
COPY . .

# Make gradlew executable
RUN chmod +x gradlew

# Build Elasticsearch distribution (this creates the tar.gz)
# Using --no-daemon to prevent Gradle daemon from running in container
# Building only the linux-tar distribution (OSS - no x-pack features)
RUN ./gradlew :distribution:archives:linux-tar:assemble --no-daemon -Dbuild.snapshot=true -Dbuild.license=oss

# Extract the built distribution
RUN mkdir -p /elasticsearch && \
    tar -xzf distribution/archives/linux-tar/build/distributions/elasticsearch-*.tar.gz -C /elasticsearch --strip-components=1

################################################################################
# Stage 2: Runtime - Create the final Elasticsearch image
################################################################################
FROM eclipse-temurin:17-jre

# Install required runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    tini \
    && rm -rf /var/lib/apt/lists/*

# Install tini as init process
# Download and verify tini binary
RUN set -eux; \
    arch="$(dpkg --print-architecture)"; \
    case "$arch" in \
        amd64) tini_bin='tini-amd64'; tini_sum='93dcc18adc78c65a028a84799ecf8ad40c936fdfc5f2a57b1acda5a8117fa82c' ;; \
        aarch64) tini_bin='tini-arm64'; tini_sum='07952557df20bfd2a95f9bef198b445e006171969499a1d361bd9e6f8e5e0e81' ;; \
        *) echo >&2 "Unsupported architecture $arch"; exit 1 ;; \
    esac; \
    curl -f --retry 10 -S -L -o /tmp/tini https://github.com/krallin/tini/releases/download/v0.19.0/${tini_bin}; \
    echo "${tini_sum}  /tmp/tini" | sha256sum -c -; \
    mv /tmp/tini /usr/bin/tini; \
    chmod +x /usr/bin/tini

# Create elasticsearch user and group (use -f to force if already exists)
RUN groupadd -f -g 1000 elasticsearch || true && \
    useradd -u 1000 -g elasticsearch -G 0 -d /usr/share/elasticsearch elasticsearch || true

# Set environment variables
ENV ELASTIC_CONTAINER=true
ENV ES_HOME=/usr/share/elasticsearch
ENV PATH=/usr/share/elasticsearch/bin:$PATH
ENV SHELL=/bin/bash

# Copy built Elasticsearch from builder stage (use numeric UID/GID)
COPY --from=builder --chown=1000:1000 /elasticsearch /usr/share/elasticsearch

# Set proper permissions and create necessary directories
RUN chmod -R 755 /usr/share/elasticsearch && \
    mkdir -p /usr/share/elasticsearch/data /usr/share/elasticsearch/logs /usr/share/elasticsearch/plugins && \
    chown -R 1000:1000 /usr/share/elasticsearch/data /usr/share/elasticsearch/logs /usr/share/elasticsearch/plugins && \
    chmod g=u /etc/passwd

# Copy the docker-entrypoint script
COPY --chmod=755 bin/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

# Replace OpenJDK's built-in CA certificate keystore with the one from the OS
# vendor. The latter is superior in several ways.
RUN ln -sf /etc/pki/ca-trust/extracted/java/cacerts /usr/share/elasticsearch/jdk/lib/security/cacerts

# Expose HTTP port (9200) and transport port (9300)
EXPOSE 9200 9300

# Set the entrypoint to tini for proper signal handling
ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/docker-entrypoint.sh"]

# Default command
CMD ["eswrapper"]

# Switch to elasticsearch user
USER 1000:1000