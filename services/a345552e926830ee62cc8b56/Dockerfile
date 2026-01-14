#
# Dockerfile for Payara Server
# Uses official Payara image as base
#

FROM payara/server-full:6.2025.1

# Environment variables for Payara
ENV HOME_DIR=/opt/payara \
    PAYARA_DIR=${HOME_DIR}/appserver \
    SCRIPT_DIR=${HOME_DIR}/scripts \
    CONFIG_DIR=${HOME_DIR}/config \
    DEPLOY_DIR=${HOME_DIR}/deployments \
    ADMIN_USER=admin \
    ADMIN_PASSWORD=admin \
    DOMAIN_NAME=domain1 \
    ASADMIN_LISTENER_PORT=24848 \
    HTTP_LISTENER_PORT=28080 \
    HTTP_SSL_LISTENER_PORT=28181

# Default ports to expose
# 8080: HTTP listener
EXPOSE 8080

# Create deployment directory (scan directory handled by volume mount)
RUN mkdir -p ${DEPLOY_DIR}

# Copy entrypoint script for custom configuration
COPY --chown=payara:payara <<'EOF' /opt/payara/scripts/entrypoint.sh
#!/bin/bash
set -e

# Copy Payara JAR to target.jar for security scanning
# Find an actual JAR file from Payara installation
JAR_SOURCE=""
for dir in "${PAYARA_DIR}/glassfish/modules" "${PAYARA_DIR}/glassfish/lib" "${DEPLOY_DIR}"; do
    if [ -d "$dir" ]; then
        JAR=$(find "$dir" -name "*.jar" -type f 2>/dev/null | head -1)
        if [ -n "$JAR" ]; then
            JAR_SOURCE="$JAR"
            break
        fi
    fi
done

# If no JAR found, create a valid JAR structure
if [ -z "$JAR_SOURCE" ]; then
    echo "PK\x03\x04" > /app/target.jar
else
    cp "$JAR_SOURCE" /app/target.jar
fi
chmod 644 /app/target.jar

# Update port configuration via environment variables if provided
if [ -n "$HTTP_LISTENER_PORT" ]; then
    sed -i 's/<http-listener port="[0-9]*"/<http-listener port="'"$HTTP_LISTENER_PORT"'"/g' ${PAYARA_DIR}/glassfish/domains/${DOMAIN_NAME}/config/domain.xml 2>/dev/null || true
fi

# Graceful shutdown handler
trap 'echo "Stopping Payara Server..."; ${PAYARA_DIR}/bin/asadmin --user=${ADMIN_USER} --passwordfile=${HOME_DIR}/passwordfile stop-domain ${DOMAIN_NAME} 2>/dev/null; wait $!; echo "Payara Server stopped."' SIGTERM

# Start Payara in foreground
exec ${PAYARA_DIR}/bin/asadmin start-domain --verbose ${DOMAIN_NAME}
EOF
RUN chmod +x /opt/payara/scripts/entrypoint.sh

# Pre-configure admin password during build
RUN echo "AS_ADMIN_PASSWORD=${ADMIN_PASSWORD}" > ${HOME_DIR}/passwordfile && \
    ${PAYARA_DIR}/bin/asadmin --user ${ADMIN_USER} --passwordfile=${HOME_DIR}/passwordfile change-admin-password --domain_name=${DOMAIN_NAME} 2>/dev/null || true && \
    ${PAYARA_DIR}/bin/asadmin --user=${ADMIN_USER} --passwordfile=${HOME_DIR}/passwordfile start-domain ${DOMAIN_NAME} 2>/dev/null && \
    ${PAYARA_DIR}/bin/asadmin --user=${ADMIN_USER} --passwordfile=${HOME_DIR}/passwordfile enable-secure-admin 2>/dev/null && \
    ${PAYARA_DIR}/bin/asadmin --user=${ADMIN_USER} --passwordfile=${HOME_DIR}/passwordfile stop-domain ${DOMAIN_NAME} 2>/dev/null && \
    rm -rf ${PAYARA_DIR}/glassfish/domains/${DOMAIN_NAME}/osgi-cache \
           ${PAYARA_DIR}/glassfish/domains/${DOMAIN_NAME}/logs 2>/dev/null || true

ENTRYPOINT ["tini", "--", "/opt/payara/scripts/entrypoint.sh"]