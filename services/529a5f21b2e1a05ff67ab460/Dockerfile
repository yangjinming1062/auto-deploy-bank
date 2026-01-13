# Liferay Portal Docker configuration
# Uses official Liferay image with custom configuration

FROM liferay/portal:latest

# Labels for metadata
LABEL maintainer="devops@example.com"
LABEL description="Liferay Portal with custom configuration"
LABEL version="7.4.x"

# Copy Docker-specific configuration to Lirector configs directory
# Configs from /mnt/liferay/configs are copied to /opt/liferay during startup
COPY docker-portal-ext.properties /mnt/liferay/configs/docker/portal-ext.properties
COPY system.properties /mnt/liferay/configs/docker/system.properties

# Also copy portal-ext.properties directly to /opt/liferay where it's expected
COPY docker-portal-ext.properties /opt/liferay/portal-ext.properties

# Copy OSGi configuration files for database settings directly to osgi/configs
# with proper permissions so liferay user can read them
COPY --chmod=644 osgi/configs/*.cfg /opt/liferay/osgi/configs/
COPY --chmod=644 osgi/configs/*.config /opt/liferay/osgi/configs/

# Note: target.jar is created via volume mount in docker-compose.yaml

# Expose Liferay ports
# 8080 - HTTP
# 8009 - AJP connector (for load balancers)
# 8005 - Tomcat shutdown port
EXPOSE 8080 8009 8005