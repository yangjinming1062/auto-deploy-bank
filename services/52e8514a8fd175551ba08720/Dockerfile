# Multi-stage build for Apache Dubbo Demo Provider
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy entire project structure
COPY . .

# Download dependencies
RUN mvn dependency:go-offline -B

# Build the provider application
RUN mvn clean package -pl dubbo-demo/dubbo-demo-api/dubbo-demo-api-provider -am -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/dubbo-demo/dubbo-demo-api/dubbo-demo-api-provider/target/dubbo-demo-api-provider-*.jar target.jar

# Copy dubbo.properties configuration
COPY dubbo.properties ./dubbo.properties

# Expose Dubbo protocol port (20880) and QoS port (22222)
EXPOSE 20880 22222

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:22222 || exit 1

# Start the application with Java 17 compatibility flags
CMD ["java", "--add-opens=java.base/java.lang=ALL-UNNAMED", "--add-opens=java.base/java.lang.invoke=ALL-UNNAMED", "--add-opens=java.base/java.lang.reflect=ALL-UNNAMED", "--add-opens=java.base/java.io=ALL-UNNAMED", "--add-opens=java.base/java.net=ALL-UNNAMED", "--add-opens=java.base/java.nio=ALL-UNNAMED", "--add-opens=java.base/java.util=ALL-UNNAMED", "--add-opens=java.base/java.util.concurrent=ALL-UNNAMED", "--add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED", "--add-opens=java.base/jdk.internal.reflect=ALL-UNNAMED", "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED", "-jar", "target.jar"]