# Multi-stage build for dcm4che-stowrsd
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy pom.xml and resolve dependencies
COPY pom.xml .
COPY dcm4che-tool/dcm4che-tool-common/pom.xml ./dcm4che-tool/dcm4che-tool-common/
COPY dcm4che-core/pom.xml ./dcm4che-core/
COPY dcm4che-mime/pom.xml ./dcm4che-mime/
COPY dcm4che-audit/pom.xml ./dcm4che-audit/
COPY dcm4che-audit-keycloak/pom.xml ./dcm4che-audit-keycloak/
COPY dcm4che-conf/pom.xml ./dcm4che-conf/
COPY dcm4che-dcmr/pom.xml ./dcm4che-dcmr/
COPY dcm4che-deident/pom.xml ./dcm4che-deident/
COPY dcm4che-dict/pom.xml ./dcm4che-dict/
COPY dcm4che-dict-priv/pom.xml ./dcm4che-dict-priv/
COPY dcm4che-emf/pom.xml ./dcm4che-emf/
COPY dcm4che-hl7/pom.xml ./dcm4che-hl7/
COPY dcm4che-image/pom.xml ./dcm4che-image/
COPY dcm4che-imageio/pom.xml ./dcm4che-imageio/
COPY dcm4che-imageio-opencv/pom.xml ./dcm4che-imageio-opencv/
COPY dcm4che-imageio-rle/pom.xml ./dcm4che-imageio-rle/
COPY dcm4che-imageio-test/pom.xml ./dcm4che-imageio-test/
COPY dcm4che-json/pom.xml ./dcm4che-json/
COPY dcm4che-js-dict/pom.xml ./dcm4che-js-dict/
COPY dcm4che-net/pom.xml ./dcm4che-net/
COPY dcm4che-net-audit/pom.xml ./dcm4che-net-audit/
COPY dcm4che-net-hl7/pom.xml ./dcm4che-net-hl7/
COPY dcm4che-net-imageio/pom.xml ./dcm4che-net-imageio/
COPY dcm4che-qstar/pom.xml ./dcm4che-qstar/
COPY dcm4che-soundex/pom.xml ./dcm4che-soundex/
COPY dcm4che-ws-rs/pom.xml ./dcm4che-ws-rs/
COPY dcm4che-xdsi/pom.xml ./dcm4che-xdsi/
COPY dcm4che-xroad/pom.xml ./dcm4che-xroad/
COPY dcm4che-tool/pom.xml ./dcm4che-tool/
COPY dcm4che-assembly/pom.xml ./dcm4che-assembly/
COPY dcm4che-jboss-modules/pom.xml ./dcm4che-jboss-modules/
COPY dcm4che-camel/pom.xml ./dcm4che-camel/
COPY dcm4che-test-data/pom.xml ./dcm4che-test-data/

# Copy source code for all modules
COPY dcm4che-tool/dcm4che-tool-stowrsd ./dcm4che-tool/dcm4che-tool-stowrsd
COPY dcm4che-tool/dcm4che-tool-common ./dcm4che-tool/dcm4che-tool-common
COPY dcm4che-core ./dcm4che-core
COPY dcm4che-mime ./dcm4che-mime
COPY dcm4che-audit ./dcm4che-audit
COPY dcm4che-audit-keycloak ./dcm4che-audit-keycloak
COPY dcm4che-conf ./dcm4che-conf
COPY dcm4che-dcmr ./dcm4che-dcmr
COPY dcm4che-deident ./dcm4che-deident
COPY dcm4che-dict ./dcm4che-dict
COPY dcm4che-dict-priv ./dcm4che-dict-priv
COPY dcm4che-emf ./dcm4che-emf
COPY dcm4che-hl7 ./dcm4che-hl7
COPY dcm4che-image ./dcm4che-image
COPY dcm4che-imageio ./dcm4che-imageio
COPY dcm4che-imageio-opencv ./dcm4che-imageio-opencv
COPY dcm4che-imageio-rle ./dcm4che-imageio-rle
COPY dcm4che-imageio-test ./dcm4che-imageio-test
COPY dcm4che-json ./dcm4che-json
COPY dcm4che-js-dict ./dcm4che-js-dict
COPY dcm4che-net ./dcm4che-net
COPY dcm4che-net-audit ./dcm4che-net-audit
COPY dcm4che-net-hl7 ./dcm4che-net-hl7
COPY dcm4che-net-imageio ./dcm4che-net-imageio
COPY dcm4che-qstar ./dcm4che-qstar
COPY dcm4che-soundex ./dcm4che-soundex
COPY dcm4che-ws-rs ./dcm4che-ws-rs
COPY dcm4che-xdsi ./dcm4che-xdsi
COPY dcm4che-xroad ./dcm4che-xroad
COPY dcm4che-tool ./dcm4che-tool
COPY dcm4che-assembly ./dcm4che-assembly
COPY dcm4che-jboss-modules ./dcm4che-jboss-modules
COPY dcm4che-camel ./dcm4che-camel
COPY dcm4che-test-data ./dcm4che-test-data
COPY etc ./etc

# Build the stowrsd tool with dependencies
RUN mvn clean package -DskipTests -B -pl :dcm4che-tool-stowrsd -am && \
    mvn dependency:copy-dependencies -DoutputDirectory=/app/target/lib -pl :dcm4che-tool-stowrsd && \
    ls -la /app/target/

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# Install wget for healthcheck and entrypoint script
USER root
RUN apk add --no-cache wget
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
# Keep running as root to populate the volume
# USER 65534

# Set working directory
WORKDIR /app

# Copy logback configuration and response.xml
COPY dcm4che-assembly/src/etc/stowrsd/logback.xml /app/logback.xml
COPY dcm4che-assembly/src/etc/stowrsd/response.xml /app/response.xml

# Copy JAR and dependencies from builder stage
COPY --from=builder /app/dcm4che-tool/dcm4che-tool-stowrsd/target/dcm4che-tool-stowrsd-*.jar /app/target.jar.image
COPY --from=builder /app/target/lib /app/lib

# Expose port 8080
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ || exit 1

# Run the application with logback configuration
ENTRYPOINT ["/entrypoint.sh"]
CMD ["java", "-Dlogback.configurationFile=/app/logback.xml", "-cp", "/app/target.jar:/app/lib/*", "org.dcm4che3.tool.stowrsd.StowRSServer", "-b", "0.0.0.0:8080"]