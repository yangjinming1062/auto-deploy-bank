# CDAP Master Service - Using local pre-built CDAP Sandbox
FROM eclipse-temurin:17-jre-alpine

# Set CDAP home
ENV CDAP_HOME=/opt/cdap/sandbox
ENV CDAP_VERSION=6.11.1

# Copy CDAP sandbox from local installation
COPY opt/cdap/sandbox-${CDAP_VERSION} /opt/cdap/sandbox-${CDAP_VERSION}
COPY opt/cdap/sandbox /opt/cdap/sandbox -> /opt/cdap/sandbox-${CDAP_VERSION}

# Copy configuration files
COPY cdap-site.xml /opt/cdap/sandbox-${CDAP_VERSION}/conf/cdap-site.xml
COPY cdap-security.xml /opt/cdap/sandbox-${CDAP_VERSION}/conf/cdap-security.xml
COPY realm.properties /opt/cdap/sandbox-${CDAP_VERSION}/conf/realm.properties
COPY hbase-site.xml /opt/cdap/sandbox-${CDAP_VERSION}/conf/hbase-site.xml
COPY hive-site.xml /opt/cdap/sandbox-${CDAP_VERSION}/conf/hive-site.xml
COPY mapred-site.xml /opt/cdap/sandbox-${CDAP_VERSION}/conf/mapred-site.xml
COPY logback.xml /opt/cdap/sandbox-${CDAP_VERSION}/conf/logback.xml

# Create symlink for current version
RUN ln -sf /opt/cdap/sandbox-${CDAP_VERSION} /opt/cdap/sandbox

# Create directories for data and logs
RUN mkdir -p /opt/cdap/sandbox/data /opt/cdap/sandbox/logs && \
    mkdir -p /cdap-jar

# Copy main CDAP JAR for security scanning - use the standalone JAR
COPY opt/cdap/sandbox-${CDAP_VERSION}/lib/io.cdap.cdap.cdap-standalone-${CDAP_VERSION}.jar /cdap-jar/target.jar
# Also copy spark pipeline JAR
COPY opt/cdap/sandbox-${CDAP_VERSION}/artifacts/spark3_2.12/cdap-data-pipeline-${CDAP_VERSION}.jar /cdap-jar/target-spark.jar 2>/dev/null || true

# Create non-root user
RUN addgroup -g 1000 cdap && \
    adduser -u 1000 -G cdap -s /bin/sh -D cdap && \
    chown -R cdap:cdap /opt/cdap/sandbox /cdap-jar

# Switch to non-root user
USER cdap

# Set working directory
WORKDIR /opt/cdap/sandbox

# Expose the main router port and SSL port
EXPOSE 11015 10443

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=180s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:11015/v3/health || exit 1

# Start CDAP Sandbox
CMD ["/opt/cdap/sandbox/bin/cdap", "sandbox", "start", "--foreground"]