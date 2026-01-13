# Multi-stage build for Spring Boot application
# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Create proper directory structure for multi-module Maven build
RUN mkdir -p spring-ai-alibaba-studio/spring-ai-alibaba-studio-server/spring-ai-alibaba-studio-server-admin

# Copy parent POMs
COPY ../../../../pom.xml ./pom.xml
COPY ../../pom.xml ./spring-ai-alibaba-studio/spring-ai-alibaba-studio-server/pom.xml

# Copy this module's pom.xml and source code
COPY pom.xml ./spring-ai-alibaba-studio/spring-ai-alibaba-studio-server/spring-ai-alibaba-studio-server-admin/pom.xml
COPY src ./spring-ai-alibaba-studio/spring-ai-alibaba-studio-server/spring-ai-alibaba-studio-admin/src

# Build the module with proper parent references
WORKDIR /app/spring-ai-alibaba-studio/spring-ai-alibaba-studio-server/spring-ai-alibaba-studio-server-admin
RUN mvn clean package -DskipTests -B

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

# Copy the built JAR from builder stage
COPY --from=builder /app/target/spring-ai-alibaba-studio-server-admin.jar app.jar

# Expose port 8080 (Spring Boot default)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/actuator/health || exit 1

# Run the application
CMD ["java", "-jar", "app.jar"]