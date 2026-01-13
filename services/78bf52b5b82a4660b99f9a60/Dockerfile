FROM eclipse-temurin:17-jdk-alpine

# Install Maven and curl for thin JAR dependencies
RUN apk --no-cache add openjdk17-jdk maven curl && \
    rm -rf /var/cache/apk/*

WORKDIR /app

# Debug: list target directory contents
RUN ls -la target/ 2>/dev/null || echo "target directory not found in build context"

# Create configuration directories
RUN mkdir -p /opt/cloudexplorer/conf /opt/cloudexplorer/logs

# Create minimal cloudexplorer.properties file
RUN echo '# CloudExplorer Configuration' > /opt/cloudexplorer/conf/cloudexplorer.properties && \
    echo 'ce.version=main' >> /opt/cloudexplorer/conf/cloudexplorer.properties && \
    echo 'ce.base=/opt/cloudexplorer' >> /opt/cloudexplorer/conf/cloudexplorer.properties

# Copy pre-built JAR files and Maven repository for thin JAR support
COPY framework/eureka/target/eureka-*.jar /app/eureka.jar
COPY framework/gateway/target/gateway-*.jar /app/gateway.jar
COPY framework/management-center/backend/target/management-center-*.jar /app/management-center.jar
COPY target/repository /root/.m2/repository

# Create startup script to run all services (using --thin.root for dependency resolution)
RUN echo '#!/bin/sh' > /app/start.sh && \
    echo 'echo "Starting CloudExplorer-Lite services..."' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo 'echo "Starting Eureka on port 8761..."' >> /app/start.sh && \
    echo 'nohup java -jar /app/eureka.jar -Dfile.encoding=utf-8 -Deureka.client.serviceUrl.defaultZone=http://eureka:8761/eureka/ > /opt/cloudexplorer/logs/eureka.log 2>&1 &' >> /app/start.sh && \
    echo 'EUREKA_PID=$!' >> /app/start.sh && \
    echo 'echo "Waiting for Eureka to start..."' >> /app/start.sh && \
    echo 'sleep 15' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo 'echo "Starting Management Center on port 9010..."' >> /app/start.sh && \
    echo 'nohup java -jar /app/management-center.jar -Dfile.encoding=utf-8 -Dce.mysql.host=mysql -Dce.redis.host=redis > /opt/cloudexplorer/logs/management-center.log 2>&1 &' >> /app/start.sh && \
    echo 'MC_PID=$!' >> /app/start.sh && \
    echo 'echo "Waiting for Management Center to start..."' >> /app/start.sh && \
    echo 'sleep 15' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo 'echo "Starting Gateway on port 9000..."' >> /app/start.sh && \
    echo 'echo "Gateway will be available at http://localhost:40057"' >> /app/start.sh && \
    echo 'nohup java -jar /app/gateway.jar -Dfile.encoding=utf-8 -Dserver.port=9000 > /opt/cloudexplorer/logs/gateway.log 2>&1 &' >> /app/start.sh && \
    echo 'GATEWAY_PID=$!' >> /app/start.sh && \
    echo 'echo "All services started"' >> /app/start.sh && \
    echo 'wait' >> /app/start.sh && \
    chmod +x /app/start.sh

# Expose all core service ports
EXPOSE 8761 9000 9010

# Health check for Gateway (main entry point)
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
  CMD curl -f http://localhost:9000/actuator/health || exit 1

# Start all services
CMD ["/app/start.sh"]