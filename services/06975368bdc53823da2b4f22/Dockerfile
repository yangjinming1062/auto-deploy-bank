# Multi-stage build for Spring Boot application
# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Build entire project to install parent POMs and all dependencies
COPY pom.xml .
COPY spring-ai-alibaba-core ./spring-ai-alibaba-core
COPY spring-ai-alibaba-graph-core ./spring-ai-alibaba-graph-core
COPY spring-ai-alibaba-studio ./spring-ai-alibaba-studio
COPY spring-ai-alibaba-bom ./spring-ai-alibaba-bom
COPY spring-ai-alibaba-mcp ./spring-ai-alibaba-mcp
COPY spring-ai-alibaba-a2a ./spring-ai-alibaba-a2a
COPY spring-ai-alibaba-agent-nacos ./spring-ai-alibaba-agent-nacos
COPY spring-ai-alibaba-observation-extension ./spring-ai-alibaba-observation-extension
COPY auto-configurations ./auto-configurations
COPY spring-ai-alibaba-spring-boot-starters ./spring-ai-alibaba-spring-boot-starters
COPY startup.sh ./startup.sh

# Build the entire project first to install all dependencies
WORKDIR /build
RUN mvn clean install -DskipTests -B -Dcheckstyle.skip=true -Dspotless.skip=true

# Build the specific admin module
WORKDIR /build/spring-ai-alibaba-studio/spring-ai-alibaba-studio-server/spring-ai-alibaba-studio-server-admin
RUN mvn clean package -DskipTests -B -Dcheckstyle.skip=true -Dspotless.skip=true

# Stage 2: Runtime image
FROM debian:bookworm-slim

# Install Java 17 and curl
RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless curl && \
    rm -rf /var/lib/apt/lists/*

# Set Java home
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Create app directory
WORKDIR /app

# Copy the built JAR from builder stage (both for running and for volume mount)
COPY --from=builder /build/spring-ai-alibaba-studio/spring-ai-alibaba-studio-server/spring-ai-alibaba-studio-server-admin/target/spring-ai-alibaba-studio-server-admin.jar app.jar
COPY --from=builder /build/spring-ai-alibaba-studio/spring-ai-alibaba-studio-server/spring-ai-alibaba-studio-server-admin/target/spring-ai-alibaba-studio-server-admin.jar target.jar

# Copy startup script
COPY --from=builder /build/startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh

# Expose port 8080 (Spring Boot default)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/actuator/health || exit 1

# Run the application via startup script
CMD ["/app/startup.sh"]