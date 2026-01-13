# Multi-stage build for Spring Boot application
# Stage 1: Copy keystore files
FROM ubuntu:22.04 AS builder

WORKDIR /app

# Copy keystore files for OAuth2
COPY cf-framework-parent/cf-ucenter/cf-ucenter-auth/src/main/resources/xc.keystore ./xc-auth.keystore
COPY cf-framework-parent/cf-ucenter/cf-ucenter-admin/src/main/resources/xc.keystore ./xc-admin.keystore

# Stage 2: Runtime image with Java 8 JDK
FROM eclipse-temurin:8-jdk

WORKDIR /app

# Install utilities
RUN apt-get update && apt-get install -y unzip wget net-tools && rm -rf /var/lib/apt/lists/*

# Copy keystore files from builder stage
COPY --from=builder /app/xc-auth.keystore ./xc-auth.keystore
COPY --from=builder /app/xc-admin.keystore ./xc-admin.keystore
COPY --from=builder /app/xc-auth.keystore ./xc.keystore

# Copy public key file for JWT verification
COPY cf-framework-parent/cf-ucenter/cf-ucenter-api/src/main/resources/publickey.txt ./publickey.txt

# Copy main JAR file
COPY target.jar ./cf-ucenter-api.jar

# Create log directory
RUN mkdir -p /app/log

# Expose ports (internal ports only)
EXPOSE 8080 8081 8082 8083 8084 8085 8086 8087 8088 8089 8090 8091 8092 8093 8094 8095

# Health check - check if Tomcat is running on port 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
  CMD netstat -tuln | grep -q ':8080 ' || exit 1

# Default CMD
CMD ["sh", "-c", "echo 'Container ready. Services will start via docker-compose command.' && tail -f /dev/null"]