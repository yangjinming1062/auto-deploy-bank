# Use official SonarQube Community image as base
FROM sonarqube:community

# Create /scanning directory for security scanning volume mount
# The JAR will be accessible at /scanning/target.jar
USER root
RUN mkdir -p /scanning && \
    # Copy the SonarQube application JAR for security scanning
    cp /opt/sonarqube/lib/sonarqube-*.jar /scanning/target.jar 2>/dev/null || \
    cp /opt/sonarqube/lib/sonar-application-*.jar /scanning/target.jar 2>/dev/null || true && \
    chmod 644 /scanning/target.jar 2>/dev/null || true && \
    chown -R 1000:0 /scanning

# Switch back to sonarqube user
USER 1000

# Expose web port and Elasticsearch port
EXPOSE 9000 9001

# Health check - verify web server is responding
HEALTHCHECK --interval=30s --timeout=30s --start-period=120s --retries=5 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:9000/ -q && exit 0 || exit 1

# Keep the original entrypoint
ENTRYPOINT ["/opt/sonarqube/docker/entrypoint.sh"]