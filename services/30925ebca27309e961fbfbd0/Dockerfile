# Multi-stage build for Apache Doris Frontend (FE)
# Stage 1: Copy JAR from official Doris FE image for security scanning
FROM apache/doris:fe-3.1.3 AS scanner

# Create app directory and copy the FE JAR for security scanning
RUN mkdir -p /app && \
    find /opt/apache-doris -name "*.jar" -type f | head -5 && \
    find /opt/apache-doris -name "doris-fe.jar" -exec cp {} /app/target.jar \; && \
    chmod 644 /app/target.jar

# Stage 2: Runtime image based on official Apache Doris FE image
FROM apache/doris:fe-3.1.3

# Copy JAR for security scanning (volume mount target)
COPY --from=scanner /app/target.jar /app/target.jar

# Copy custom configuration
COPY conf/fe.conf /opt/apache-doris/fe/conf/

# Copy web UI static resources
COPY webroot/ /opt/apache-doris/fe/webroot/

# Copy custom start script (optional overrides)
COPY bin/start_fe.sh /opt/apache-doris/fe/bin/start_fe.sh
COPY bin/stop_fe.sh /opt/apache-doris/fe/bin/stop_fe.sh

# Make scripts executable
RUN chmod +x /opt/apache-doris/fe/bin/*.sh && \
    chmod +x /usr/local/bin/init_fe.sh

# Set environment variables
ENV DORIS_HOME=/opt/apache-doris
ENV FE_HOME=/opt/apache-doris/fe
ENV LOG_DIR=${FE_HOME}/log
ENV DORIS_LOG_TO_STDERR=1
# Ensure Java 17 is used (using symlink which points to jdk-17)
ENV JAVA_HOME=/usr/lib/jvm/java
ENV PATH=$PATH:$JAVA_HOME/bin:${FE_HOME}/bin

# Create log directory
RUN mkdir -p ${LOG_DIR}

# Expose ports (HTTP, RPC, Query, Edit Log, Arrow Flight SQL)
EXPOSE 8030 9020 9030 9010 8070

# Health check - Doris FE HTTP port (web UI)
HEALTHCHECK --interval=30s --timeout=15s --start-period=120s --retries=5 \
  CMD wget --quiet --tries=1 --spider http://localhost:8030/ || exit 1

# Start the FE service in foreground using init_fe.sh
CMD ["/usr/local/bin/init_fe.sh"]