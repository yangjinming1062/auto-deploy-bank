# Multi-stage build for Apache StreamPark Console Service

# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /build

# Copy pom.xml first for better layer caching
COPY pom.xml .

# Copy module pom.xml files
COPY streampark-console/pom.xml streampark-console/
COPY streampark-console/streampark-console-service/pom.xml streampark-console/streampark-console-service/
COPY streampark-common/pom.xml streampark-common/
COPY streampark-flink/pom.xml streampark-flink/
COPY streampark-spark/pom.xml streampark-spark/

# Copy all source code directories first
COPY streampark-common streampark-common
COPY streampark-flink streampark-flink
COPY streampark-spark streampark-spark
COPY streampark-console streampark-console
COPY tools tools

# Build the entire project first (skip spotless and tests)
RUN mvn clean install -DskipTests -Dspotless.check.skip=true -Dcheckstyle.skip=true -B

# Package the console service with assembly (creates distribution)
RUN cd streampark-console/streampark-console-service \
    && mvn package -DskipTests -Dspotless.check.skip=true -Dcheckstyle.skip=true -B

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre

# Install bash and netcat for startup script and health check
RUN apt-get update && apt-get install -y \
    bash \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/lib /app/conf /app/logs /app/temp

# Copy the assembly distribution (extract contents to /app/)
COPY --from=builder /build/streampark-console/streampark-console-service/target/apache-streampark-2.2.0-SNAPSHOT-bin/* /app/

# Remove only specific conflicting versions (keep Spring Boot and core dependencies)
RUN cd /app/lib \
    && rm -f slf4j-nop-*.jar slf4j-jdk14-*.jar \
    && rm -f slf4j-simple-*.jar \
    && rm -f slf4j-log4j12-*.jar \
    && rm -f log4j-*.jar log4j-over-slf4j-*.jar \
    && rm -f jcl-over-slf4j-*.jar jul-to-slf4j-*.jar \
    && rm -f logback-classic-1.1.2.jar logback-core-1.1.2.jar \
    && rm -f commons-collections-3.1.jar commons-collections-3.2.jar commons-collections-3.2.1.jar \
    && rm -f jetty-6.*.jar \
    && rm -f jetty-*-9.2.*.jar jetty-*-9.3.24.*.jar jetty-*-9.3.27.*.jar \
    && rm -f jetty-util-ajax-9.3.*.jar \
    && rm -f nexus-staging-maven-plugin-*.jar \
    && rm -f httpcore-4.0.1.jar httpcore-4.1.2.jar httpcore-4.2.4.jar httpcore-4.2.5.jar httpcore-4.3.2.jar httpcore-4.4.4.jar \
    && rm -f httpcore5-5.1.1.jar httpcore5-h2-5.1.1.jar

# Make startup scripts executable
RUN chmod +x /app/bin/*.sh

# Copy JAR file for security scanning
RUN cp /app/lib/streampark-console-service-*.jar /app/target.jar

# Set environment variables
ENV APP_HOME=/app
ENV JAVA_HOME=/opt/java/openjdk
ENV SERVER_PORT=10000
ENV JAVA_OPTS="--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.invoke=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED"

# Expose the service port
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD nc -z localhost 10000 || exit 1

# Run the application using the official startup script
CMD ["/app/bin/streampark.sh", "start_docker"]