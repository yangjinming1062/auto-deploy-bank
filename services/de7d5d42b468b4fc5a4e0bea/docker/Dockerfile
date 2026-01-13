# Multi-stage build for SuperSonic

# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-21 AS builder

# Set working directory
WORKDIR /build

# Copy pom.xml and source code
COPY pom.xml .
COPY . .

# Build the project (skip tests for faster build)
# Dependencies will be downloaded as needed during build
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage
FROM eclipse-temurin:21-jre

# Install bash, wget, C++ standard library, and all ONNX runtime dependencies
RUN apt-get update && apt-get install -y bash wget libstdc++6 libgcc-s1 libc6 libgomp1 libatomic1 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /usr/src/app

# Copy and extract the assembled distribution
COPY --from=builder /build/launchers/standalone/target/*-bin.tar.gz .
RUN tar -xzf *-bin.tar.gz && rm *-bin.tar.gz

# Find and rename the extracted directory
RUN mv launchers-standalone-* supersonic-standalone-latest

# Set working directory to the application
WORKDIR /usr/src/app/supersonic-standalone-latest

# Make the daemon script executable
RUN chmod +x bin/supersonic-daemon.sh

# Create symbolic link for security scanning to /app/target.jar
RUN mkdir -p /app && ln -sf /usr/src/app/supersonic-standalone-latest/supersonic-standalone-*.jar /app/target.jar

# Expose the application port
EXPOSE 9080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:9080/actuator/health || exit 1

# Run the application using java directly with proper classpath
# Use JAVA_OPTS environment variable for configuration
CMD ["bash", "-c", "eval 'echo $JAVA_OPTS' && java $JAVA_OPTS -cp 'lib/*' com.tencent.supersonic.StandaloneLauncher --spring.profiles.active=h2 --server.port=9080"]