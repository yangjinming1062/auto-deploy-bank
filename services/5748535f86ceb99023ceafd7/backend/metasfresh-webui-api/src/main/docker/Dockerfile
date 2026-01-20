# Multi-stage build for metasfresh-webui-api

# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy pom.xml and download dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin-17-jre-alpine

WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /build/target/*.jar app.jar

# Copy configuration files
COPY src/main/configs/metasfresh.properties ./metasfresh.properties

# Create directory for exploded JAR
RUN mkdir -p /app/BOOT-INF/classes && \
    unzip -q app.jar -d /app/BOOT-INF/classes 2>/dev/null || true

# Create symlink for backward compatibility
RUN ln -s /app/app.jar /app/target.jar

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/actuator/health || exit 1

# Run the application
CMD ["java", \
     "-Xmx512M", \
     "-XX:+HeapDumpOnOutOfMemoryError", \
     "-Dsun.misc.URLClassPath.disableJarChecking=true", \
     "-Dspring.data.elasticsearch.cluster-nodes=${ES_HOST:-search}:${ES_PORT:-9300}", \
     "-Dspring.rabbitmq.host=${RABBITMQ_HOST:-rabbitmq}", \
     "-Dspring.rabbitmq.port=${RABBITMQ_PORT:-5672}", \
     "-Dspring.rabbitmq.username=${RABBITMQ_USER:-metasfresh}", \
     "-Dspring.rabbitmq.password=${RABBITMQ_PASSWORD:-metasfresh}", \
     "-Dloader.path=/opt/metasfresh/external-lib", \
     "-DPropertyFile=/app/metasfresh.properties", \
     "-Djava.security.egd=file:/dev/./urandom", \
     "-jar", "app.jar"]