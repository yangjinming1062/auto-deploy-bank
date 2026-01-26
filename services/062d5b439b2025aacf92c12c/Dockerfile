# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy entire project structure for proper Maven multi-module build
COPY pom.xml .
COPY powerjob-common/pom.xml powerjob-common/pom.xml
COPY powerjob-client/pom.xml powerjob-client/pom.xml
COPY powerjob-remote/pom.xml powerjob-remote/pom.xml
COPY powerjob-remote/powerjob-remote-framework/pom.xml powerjob-remote/powerjob-remote-framework/pom.xml
COPY powerjob-remote/powerjob-remote-impl-http/pom.xml powerjob-remote/powerjob-remote-impl-http/pom.xml
COPY powerjob-remote/powerjob-remote-impl-akka/pom.xml powerjob-remote/powerjob-remote-impl-akka/pom.xml
COPY powerjob-worker/pom.xml powerjob-worker/pom.xml
COPY powerjob-worker-agent/pom.xml powerjob-worker-agent/pom.xml
COPY powerjob-worker-spring-boot-starter/pom.xml powerjob-worker-spring-boot-starter/pom.xml
COPY powerjob-worker-samples/pom.xml powerjob-worker-samples/pom.xml
COPY powerjob-official-processors/pom.xml powerjob-official-processors/pom.xml
COPY powerjob-server/pom.xml powerjob-server/pom.xml
COPY powerjob-server/powerjob-server-common/pom.xml powerjob-server/powerjob-server-common/pom.xml
COPY powerjob-server/powerjob-server-remote/pom.xml powerjob-server/powerjob-server-remote/pom.xml
COPY powerjob-server/powerjob-server-persistence/pom.xml powerjob-server/powerjob-server-persistence/pom.xml
COPY powerjob-server/powerjob-server-extension/pom.xml powerjob-server/powerjob-server-extension/pom.xml
COPY powerjob-server/powerjob-server-migrate/pom.xml powerjob-server/powerjob-server-migrate/pom.xml
COPY powerjob-server/powerjob-server-core/pom.xml powerjob-server/powerjob-server-core/pom.xml
COPY powerjob-server/powerjob-server-monitor/pom.xml powerjob-server/powerjob-server-monitor/pom.xml
COPY powerjob-server/powerjob-server-auth/pom.xml powerjob-server/powerjob-server-auth/pom.xml
COPY powerjob-server/powerjob-server-starter/pom.xml powerjob-server/powerjob-server-starter/pom.xml

# Copy source directories (only those that exist)
COPY powerjob-common/src powerjob-common/src
COPY powerjob-client/src powerjob-client/src
COPY powerjob-remote/powerjob-remote-framework/src powerjob-remote/powerjob-remote-framework/src
COPY powerjob-remote/powerjob-remote-impl-http/src powerjob-remote/powerjob-remote-impl-http/src
COPY powerjob-remote/powerjob-remote-impl-akka/src powerjob-remote/powerjob-remote-impl-akka/src
COPY powerjob-worker/src powerjob-worker/src
COPY powerjob-worker-agent/src powerjob-worker-agent/src
COPY powerjob-worker-spring-boot-starter/src powerjob-worker-spring-boot-starter/src
COPY powerjob-worker-samples/src powerjob-worker-samples/src
COPY powerjob-official-processors/src powerjob-official-processors/src
COPY powerjob-server/powerjob-server-common/src powerjob-server/powerjob-server-common/src
COPY powerjob-server/powerjob-server-remote/src powerjob-server/powerjob-server-remote/src
COPY powerjob-server/powerjob-server-persistence/src powerjob-server/powerjob-server-persistence/src
COPY powerjob-server/powerjob-server-extension/src powerjob-server/powerjob-server-extension/src
COPY powerjob-server/powerjob-server-migrate/src powerjob-server/powerjob-server-migrate/src
COPY powerjob-server/powerjob-server-core/src powerjob-server/powerjob-server-core/src
COPY powerjob-server/powerjob-server-monitor/src powerjob-server/powerjob-server-monitor/src
COPY powerjob-server/powerjob-server-auth/src powerjob-server/powerjob-server-auth/src
COPY powerjob-server/powerjob-server-starter/src powerjob-server/powerjob-server-starter/src

# Build the project
RUN mvn clean package -DskipTests -B -f powerjob-server/powerjob-server-starter/pom.xml

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

# Set timezone
ENV TZ=Asia/Shanghai

# Create non-root user for security
RUN addgroup -S powerjob && adduser -S powerjob -G powerjob

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/powerjob-server/powerjob-server-starter/target/powerjob-server-starter-*.jar app.jar

# Create data directory
RUN mkdir -p /root/powerjob && chown -R powerjob:powerjob /app /root/powerjob

# Switch to non-root user
USER powerjob

# Expose ports
EXPOSE 7700 10086 10010

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:7700/actuator/health || exit 1

# Start the application
CMD ["java", "-Xmx512m", "-jar", "app.jar"]