# Multi-stage build for Oracle Coherence Community Edition
# Stage 1: Build with Maven
# Note: moditect-maven-plugin requires Java 20+, using JDK 21
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /build

# Copy the entire prj directory to preserve Maven module structure
COPY prj/ ./prj/

# Copy ext directory for license file
COPY ext/ ./ext/

# Build the coherence module (which includes all dependencies in the uber-jar)
RUN mvn install -DskipTests -B -N -Pmodules -f prj/pom.xml && \
    mvn install -DskipTests -B -Pmodules -pl coherence-bom -am -f prj/pom.xml && \
    mvn package -DskipTests -B -Pmodules -pl coherence -am -f prj/pom.xml

# Stage 2: Download HTTP Netty dependencies for runtime
FROM maven:3.9-eclipse-temurin-21 AS http-deps
WORKDIR /download

# Download all required JARs for HTTP management support
RUN mkdir -p /download/libs && \
    cd /download/libs && \
    # Jersey/JAX-RS dependencies
    curl -sLO https://repo1.maven.org/maven2/org/glassfish/jersey/core/jersey-server/3.1.9/jersey-server-3.1.9.jar && \
    curl -sLO https://repo1.maven.org/maven2/org/glassfish/jersey/inject/jersey-hk2/3.1.9/jersey-hk2-3.1.9.jar && \
    curl -sLO https://repo1.maven.org/maven2/org/glassfish/jersey/media/jersey-media-json-jackson/3.1.9/jersey-media-json-jackson-3.1.9.jar && \
    curl -sLO https://repo1.maven.org/maven2/org/glassfish/jersey/common/jersey-common/3.1.9/jersey-common-3.1.9.jar && \
    # Netty dependencies
    curl -sLO https://repo1.maven.org/maven2/io/netty/netty-codec-http/4.1.114/netty-codec-http-4.1.114.Final.jar && \
    curl -sLO https://repo1.maven.org/maven2/io/netty/netty-codec/4.1.114/netty-codec-4.1.114.Final.jar && \
    curl -sLO https://repo1.maven.org/maven2/io/netty/netty-handler/4.1.114/netty-handler-4.1.114.Final.jar && \
    curl -sLO https://repo1.maven.org/maven2/io/netty/netty-buffer/4.1.114/netty-buffer-4.1.114.Final.jar && \
    curl -sLO https://repo1.maven.org/maven2/io/netty/netty-transport/4.1.114/netty-transport-4.1.114.Final.jar && \
    curl -sLO https://repo1.maven.org/maven2/io/netty/netty-resolver/4.1.114/netty-resolver-4.1.114.Final.jar && \
    curl -sLO https://repo1.maven.org/maven2/io/netty/netty-common/4.1.114/netty-common-4.1.114.Final.jar && \
    # Jackson dependencies
    curl -sLO https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-core/2.18.3/jackson-core-2.18.3.jar && \
    curl -sLO https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-databind/2.18.3/jackson-databind-2.18.3.jar && \
    curl -sLO https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-annotations/2.18.3/jackson-annotations-2.18.3.jar && \
    curl -sLO https://repo1.maven.org/maven2/com/fasterxml/jackson/module/jackson-module-parameter-names/2.18.3/jackson-module-parameter-names-2.18.3.jar && \
    # Jakarta dependencies
    curl -sLO https://repo1.maven.org/maven2/jakarta/ws/rs/jakarta.ws.rs-api/2.1.6/jakarta.ws.rs-api-2.1.6.jar && \
    curl -sLO https://repo1.maven.org/maven2/jakarta/xml/bind/jakarta.xml.bind-api/4.0.2/jakarta.xml.bind-api-4.0.2.jar && \
    curl -sLO https://repo1.maven.org/maven2/jakarta/activation/jakarta.activation-api/2.3.3/jakarta.activation-api-2.3.3.jar && \
    curl -sLO https://repo1.maven.org/maven2/jakarta/inject/jakarta.inject-api/2.0.1/jakarta.inject-api-2.0.1.jar && \
    # HK2 dependencies (required by jersey-hk2)
    curl -sLO https://repo1.maven.org/maven2/org/glassfish/jersey/core/jersey-client/3.1.9/jersey-client-3.1.9.jar && \
    curl -sLO https://repo1.maven.org/maven2/org/glassfish/hk2/hk2-api/3.0.6/hk2-api-3.0.6.jar && \
    curl -sLO https://repo1.maven.org/maven2/org/glassfish/hk2/hk2-locator/3.0.6/hk2-locator-3.0.6.jar && \
    curl -sLO https://repo1.maven.org/maven2/org/glassfish/hk2/hk2-utils/3.0.6/hk2-utils-3.0.6.jar && \
    curl -sLO https://repo1.maven.org/maven2/org/glassfish/hk2/aopli/3.0.6/aopli-3.0.6.jar && \
    curl -sLO https://repo1.maven.org/maven2/org/glassfish/hk2/hk2-core/3.0.6/hk2-core-3.0.6.jar && \
    # Javassist (required by HK2)
    curl -sLO https://repo1.maven.org/maven2/org/javassist/javassist/3.30.2-GA/javassist-3.30.2-GA.jar && \
    # OSGi
    curl -sLO https://repo1.maven.org/maven2/org/osgi/org.osgi.core/8.0.0/org.osgi.core-8.0.0.jar && \
    curl -sLO https://repo1.maven.org/maven2/org/osgi/org.osgi.compendium/8.0.0/org.osgi.compendium-8.0.0.jar

# Create license JAR for Coherence Community Edition
FROM builder AS license-builder
RUN mkdir -p /tmp/license-jar && \
    cp ext/license/coherence-community.xml /tmp/license-jar/ && \
    cd /tmp/license-jar && \
    echo "Manifest-Version: 1.0" > MANIFEST.MF && \
    jar cfm coherence-license.jar MANIFEST.MF coherence-community.xml

# Stage 3: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install wget and curl for health check
RUN apk add --no-cache wget curl bash

# Copy the built JAR from builder stage
# Use wildcard to find the coherence JAR (pattern: coherence-*.jar)
COPY --from=builder /build/prj/coherence/target/coherence-*.jar target.jar

# Copy license JAR from license-builder stage
COPY --from=license-builder /tmp/license-jar/coherence-license.jar /app/license.jar

# Copy HTTP dependencies from http-deps stage
COPY --from=http-deps /download/libs/*.jar /app/lib/

# Copy configuration files
COPY tangosol-coherence.xml /app/tangosol-coherence.xml
COPY coherence-cache-config.xml /app/coherence-cache-config.xml
COPY pof-config.xml /app/pof-config.xml

# Set environment variables for Coherence configuration
ENV COHERENCE_CLUSTER=coherence
ENV COHERENCE_MODE=dev
ENV COHERENCE_EDITION=CE
ENV COHERENCE_SECURITY=false
ENV COHERENCE_WKA=
ENV COHERENCE_LOCALHOST=
ENV COHERENCE_LOCALPORT=0
ENV COHERENCE_CLUSTERADDRESS=239.192.0.0
ENV COHERENCE_CLUSTERPORT=7574
ENV COHERENCE_SOCKETPROVIDER=system
ENV COHERENCE_DISTRIBUTED_LOCALSTORAGE=true
ENV COHERENCE_DISTRIBUTED_PARTITIONCOUNT=257
ENV COHERENCE_DISTRIBUTED_BACKUPCOUNT=1
ENV COHERENCE_PROXY_THREADS=
ENV COHERENCE_MANAGEMENT=dynamic
ENV COHERENCE_MANAGEMENT_HTTP=all
ENV COHERENCE_LOG=stderr
ENV COHERENCE_LOG_LEVEL=5
ENV COHERENCE_CACHECONFIG=coherence-cache-config.xml
ENV COHERENCE_POF_CONFIG=pof-config.xml
ENV COHERENCE_SECURITY_KEYSTORE=
ENV COHERENCE_SECURITY_PASSWORD=

# Health check configuration
ENV COHERENCE_HEALTH_HTTP_PORT=6676

# Expose health check port and internal cluster communication ports
EXPOSE 6676
EXPOSE 7574
EXPOSE 1408
EXPOSE 20000
EXPOSE 30000
EXPOSE 9612

# Health check using curl
HEALTHCHECK --start-period=30s --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://127.0.0.1:6676/ready || exit 1

# Run Coherence with HTTP management support (include lib jars in classpath)
CMD ["java", "-cp", "/app/target.jar:/app/lib/*:/app/license.jar", "com.tangosol.net.Coherence"]