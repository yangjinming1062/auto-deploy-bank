# Root Dockerfile for guide-rpc-framework
# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-8 as builder

# Set working directory
WORKDIR /app

# Copy parent POM and all module POMs
COPY pom.xml .
COPY rpc-framework-common/pom.xml rpc-framework-common/
COPY hello-service-api/pom.xml hello-service-api/
COPY rpc-framework-simple/pom.xml rpc-framework-simple/
COPY example-client/pom.xml example-client/
COPY example-server/pom.xml example-server/

# Copy source code for all modules
COPY rpc-framework-common/src rpc-framework-common/src
COPY hello-service-api/src hello-service-api/src
COPY rpc-framework-simple/src rpc-framework-simple/src
COPY example-client/src example-client/src
COPY example-server/src example-server/src

# Build all modules at once in dependency order
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM maven:3.9-eclipse-temurin-8

# Install netcat for health checks
RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create target directory
RUN mkdir -p /app/target

# Copy the built shaded JAR from builder stage
# Copy to both /app/target.jar (for volume mount) and /app/target/target.jar (for backup)
COPY --from=builder /app/example-server/target/*-shaded.jar /app/target.jar
COPY --from=builder /app/example-server/target/*-shaded.jar /app/target/target.jar

# Expose the RPC server port
EXPOSE 9998

# Health check using TCP check instead of HTTP
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD nc -z localhost 9998 || exit 1

# Override the default Maven entrypoint to run our Java application
ENTRYPOINT ["java", "-jar", "/app/target/target.jar"]
