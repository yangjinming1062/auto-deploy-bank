# Seata Server Dockerfile - Simplified Version
FROM eclipse-temurin:17-jre-alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Set working directory
WORKDIR /app

# Create directories
RUN mkdir -p /app/lib /app/logs

# Copy the Seata server JAR
COPY server/target/seata-server-1.8.0.jar app.jar

# Copy additional Seata module JARs needed for runtime
COPY all/target/seata-all-1.8.0.jar seata-all.jar
COPY seata-spring-autoconfigure/seata-spring-autoconfigure-core/target/seata-spring-autoconfigure-core-1.8.0.jar seata-spring-autoconfigure-core.jar
COPY seata-spring-autoconfigure/seata-spring-autoconfigure-server/target/seata-spring-autoconfigure-server-1.8.0.jar seata-spring-autoconfigure-server.jar
COPY console/target/seata-console-1.8.0.jar seata-console.jar

# Copy Netty NIO dependencies (version 4.1.29.Final - matches Seata)
# Note: No epoll dependencies needed as we force NIO transport
COPY netty-libs/*.jar /app/lib/

# Copy Spring Boot dependencies
COPY spring-libs/*.jar /app/lib/

# Copy remaining dependencies from local Maven repository
COPY jjwt-api-0.11.5.jar jjwt-impl-0.11.5.jar jjwt-jackson-0.11.5.jar javax.annotation-api-1.3.2.jar jcommander-1.82.jar /app/lib/

# Expose ports
EXPOSE 7091 8091

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:7091/api/v1/heartbeat || exit 1

# Start the application with all JARs in classpath, forcing NIO transport
# Disable native transport explicitly to avoid epoll dependencies
CMD ["java", \
     "-Dtransport.server=NIO", \
     "-Dio.netty.noNative=true", \
     "-Dio.netty.noEpoll=true", \
     "-Dseata.server.servicePort=8091", \
     "-cp", "app.jar:seata-all.jar:seata-spring-autoconfigure-core.jar:seata-spring-autoconfigure-server.jar:seata-console.jar:/app/lib/*", \
     "io.seata.server.ServerApplication"]