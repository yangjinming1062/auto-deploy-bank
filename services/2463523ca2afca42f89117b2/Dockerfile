# Multi-stage build for DSpace
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

# Increase Maven heap space to avoid OOM during WAR creation
ENV MAVEN_OPTS=-Xmx4g

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml /app/
RUN mvn dependency:go-offline -B

# Copy source code
COPY dspace /app/dspace
COPY dspace-api /app/dspace-api
COPY dspace-services /app/dspace-services
COPY dspace-server-webapp /app/dspace-server-webapp
COPY dspace/modules /app/dspace/modules
COPY dspace-iiif /app/dspace-iiif
COPY dspace-oai /app/dspace-oai
COPY dspace-saml2 /app/dspace-saml2
COPY dspace-rdf /app/dspace-rdf
COPY dspace-sword /app/dspace-sword
COPY dspace-swordv2 /app/dspace-swordv2

# Build the project (skip tests and validation checks)
RUN mvn clean package -DskipTests -DskipUnitTests=true -DskipIntegrationTests=true \
    -P-test-environment -Denforcer.skip=true -Dcheckstyle.skip=true \
    -Dlicense.skip=true -Dxml.skip=true -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# NOTE: DSPACE_INSTALL must align with the "dspace.dir" default configuration.
ENV DSPACE_INSTALL=/dspace

# Create dspace directory
RUN mkdir -p $DSPACE_INSTALL

# Copy the built installer from builder (copy directory contents to dspace)
COPY --from=builder /app/dspace/target/dspace-installer/ $DSPACE_INSTALL/

# Copy local.cfg to the config directory
COPY local.cfg $DSPACE_INSTALL/config/local.cfg

# Patch hibernate.cfg.xml to disable schema creation (let Flyway handle it)
# NOTE: Flyway will manage the database schema. Hibernate will only validate.
RUN sed -i 's/<property name="hibernate.hbm2ddl.auto">validate<\/property>/<property name="hibernate.hbm2ddl.auto">none<\/property>/' $DSPACE_INSTALL/config/hibernate.cfg.xml

WORKDIR $DSPACE_INSTALL

# Create necessary runtime directories
RUN mkdir -p $DSPACE_INSTALL/log && \
    mkdir -p $DSPACE_INSTALL/var/workflow && \
    mkdir -p $DSPACE_INSTALL/reader-tasks

# Install host command for "[dspace]/bin/make-handle-config" and curl for health checks
RUN apk add --no-cache bind-tools curl

# Create app directory for security scanning
RUN mkdir -p /app

# Copy the server-boot.jar for security scanning at /app/target.jar
COPY --from=builder /app/dspace/target/dspace-installer/webapps/server-boot.jar /app/target.jar

# Copy startup script
COPY start-dspace.sh /usr/local/bin/start-dspace.sh
RUN chmod +x /usr/local/bin/start-dspace.sh

# Expose Tomcat port (8080)
EXPOSE 8080

# Give java extra memory (2GB)
ENV JAVA_OPTS=-Xmx2000m

# Use container-friendly logging (console output instead of file-based)
ENV LOGGING_CONFIG=/dspace/config/log4j2-container.xml

# On startup, run DSpace startup script (initializes Solr then starts the app)
ENTRYPOINT ["/usr/local/bin/start-dspace.sh"]
