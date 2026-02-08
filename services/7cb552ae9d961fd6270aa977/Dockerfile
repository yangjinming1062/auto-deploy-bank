# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy all source files first (multi-module project needs all modules)
COPY . .

# Build the project and copy dependencies (skip tests as per instructions)
RUN mvn clean package dependency:copy-dependencies -DoutputDirectory=target/lib -DincludeScope=runtime -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built JAR files from builder stage
# The project builds multiple JARs, we'll copy them all
COPY --from=builder /app/zyt-rpc-*/target/*.jar ./

# Copy Maven dependencies
COPY --from=builder /app/zyt-rpc-*/target/lib ./lib

# Copy configuration files
COPY zyt-rpc-common/src/main/resources/*.properties ./resources/
RUN mkdir -p ./resources && cp zyt-rpc-common/src/main/resources/spring-mybatis.xml ./resources/ 2>/dev/null || true

# Create startup script that copies JAR to /data directory for security scanning
RUN cat > /app/start.sh << 'EOF'
#!/bin/sh
echo "Starting RPC Provider..."

# Copy the main JAR to /data/target.jar for security scanning (before volume mount)
mkdir -p /data
cp /app/zyt-rpc-provider-1.0-SNAPSHOT.jar /data/target.jar

# Default port if not provided
PORT=${PORT:-8080}
HOST=${HOST:-0.0.0.0}

# Find and run the provider bootstrap
exec java -cp "zyt-rpc-provider-1.0-SNAPSHOT.jar:zyt-rpc-common-1.0-SNAPSHOT.jar:zyt-rpc-api-1.0-SNAPSHOT.jar:lib/*:resources" \
  -Dlog4j.configuration=file:./resources/log4j.properties \
  provider.bootstrap.netty.NettyProviderBootStrap20 $HOST $PORT
EOF
RUN chmod +x /app/start.sh

# Set working directory
WORKDIR /app

# Expose the RPC port
EXPOSE 8080

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD nc -z localhost 8080 || exit 1

# Start the application
CMD ["/app/start.sh"]