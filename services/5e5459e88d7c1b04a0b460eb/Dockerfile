# Multi-stage build for Alluxio
# Stage 1: Build with Maven (just for JAR extraction)
FROM maven:3.9-eclipse-temurin-8 AS builder

# Install git for build
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy Maven configuration files first (for dependency caching)
COPY pom.xml .
COPY core/pom.xml core/
COPY job/pom.xml job/
COPY table/pom.xml table/
COPY shaded/pom.xml shaded/
COPY underfs/pom.xml underfs/
COPY assembly/pom.xml assembly/
COPY examples/pom.xml examples/
COPY integration/pom.xml integration/
COPY logserver/pom.xml logserver/
COPY microbench/pom.xml microbench/
COPY minicluster/pom.xml minicluster/
COPY shell/pom.xml shell/
COPY stress/pom.xml stress/
COPY tests/pom.xml tests/
COPY webui/pom.xml webui/

# Copy source code
COPY core/ core/
COPY job/ job/
COPY table/ table/
COPY shaded/ shaded/
COPY underfs/ underfs/
COPY bin/ bin/
COPY conf/ conf/
COPY build/ build/
COPY libexec/ libexec/
COPY examples/ examples/
COPY integration/ integration/
COPY dev/ dev/
COPY docs/ docs/
COPY shell/ shell/
COPY stress/ stress/
COPY tests/ tests/
COPY webui/ webui/
COPY assembly/ assembly/
COPY minicluster/ minicluster/
COPY logserver/ logserver/
COPY microbench/ microbench/
COPY templates/ templates/

# Make build scripts executable
RUN find /build/build -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true

# Initialize git repository for build (required for version info)
RUN cd /build && git init && \
    git config user.email "build@alluxio.com" && \
    git config user.name "Alluxio Builder" && \
    git add -A && \
    git commit -m "Initial commit" || true

# Build Alluxio (skip tests and quality checks for faster build)
RUN mvn clean install -DskipTests \
    -Dmaven.javadoc.skip=true \
    -Dfindbugs.skip=true \
    -Dcheckstyle.skip=true \
    -Dlicense.skip=true \
    -Dpl.project13.maven.git-commit-id-plugin.failOnNoGitDirectory=false \
    -T 2C \
    -B -q

# Stage 2: Runtime image
FROM eclipse-temurin:8-jre-alpine

# Install dependencies for Alluxio
RUN apk add --no-cache bash fuse3 libstdc++ ncurses busybox-extras wget curl

# Create alluxio user and directories
RUN addgroup -g 1000 alluxio && \
    adduser -D -u 1000 -G alluxio alluxio && \
    mkdir -p /opt/alluxio/journal /opt/alluxio/metastore /mnt/alluxio-fuse /tmp/alluxio/logs /underFSStorage /app && \
    chown -R alluxio:alluxio /opt/alluxio/journal /opt/alluxio/metastore /mnt/alluxio-fuse /tmp/alluxio /underFSStorage /app

# Download pre-built Alluxio distribution (includes all UFS modules)
ENV ALLUXIO_VERSION="2.9.1"
RUN wget -q -O /tmp/alluxio.tar.gz https://downloads.alluxio.io/downloads/files/${ALLUXIO_VERSION}/alluxio-${ALLUXIO_VERSION}-bin.tar.gz && \
    mkdir -p /opt && \
    tar -xzf /tmp/alluxio.tar.gz -C /opt && \
    rm /tmp/alluxio.tar.gz && \
    (cd /opt && rm -rf alluxio && ln -s alluxio-${ALLUXIO_VERSION} alluxio) && \
    chown -R alluxio:alluxio /opt/alluxio-${ALLUXIO_VERSION}

# Copy built JAR files from builder for security scanning
COPY --from=builder /build/assembly/server/target/alluxio-assembly-server-*-jar-with-dependencies.jar /app/target.jar
COPY --from=builder /build/assembly/client/target/alluxio-assembly-client-*-jar-with-dependencies.jar /opt/alluxio/lib/

# Copy configuration files
COPY --from=builder /build/conf/alluxio-site.properties /opt/alluxio/conf/alluxio-site.properties
COPY --from=builder /build/conf/log4j.properties /opt/alluxio/conf/log4j.properties
COPY --from=builder /build/conf/metrics.properties /opt/alluxio/conf/metrics.properties
COPY --from=builder /build/conf/core-site.xml /opt/alluxio/conf/core-site.xml
COPY --from=builder /build/conf/rocks-*.ini /opt/alluxio/conf/

# Fix permissions so alluxio user can write to conf directory
RUN chmod -R u+rw /opt/alluxio/conf/ && chown -R alluxio:alluxio /opt/alluxio/conf/

# Copy entrypoint scripts
COPY extract-jar.sh /usr/local/bin/extract-jar.sh
COPY run-alluxio.sh /usr/local/bin/run-alluxio.sh
RUN chmod +x /usr/local/bin/extract-jar.sh /usr/local/bin/run-alluxio.sh && \
    chown alluxio:alluxio /usr/local/bin/run-alluxio.sh /usr/local/bin/extract-jar.sh

# Set working directory
WORKDIR /opt/alluxio

# Switch to alluxio user
USER alluxio

# Expose Alluxio Web UI port (19999 for Web UI, 19998 for RPC)
EXPOSE 19999 19998

# Health check - check if master web UI is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:19999/ || exit 1

# Set environment variables
ENV JAVA_HOME=/opt/java/openjdk
ENV ALLUXIO_HOME=/opt/alluxio
ENV ALLUXIO_CONF_DIR=/opt/alluxio/conf
ENV PATH=/opt/alluxio/bin:$PATH
ENV LANG=en_US.UTF-8

# Start Alluxio using entrypoint script
CMD ["/usr/local/bin/extract-jar.sh"]