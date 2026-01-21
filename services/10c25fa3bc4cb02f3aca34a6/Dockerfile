# Stage 1: Builder - download dependencies and build the application
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy pom.xml, lib/ directory, and source code
COPY pom.xml .
COPY lib/ ./lib/
COPY src ./src

# Build the application (dependencies will be downloaded on-demand during build)
# The zdh_rqueue dependency is available from local lib/ directory
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime - minimal JRE image for running the application
FROM eclipse-temurin:8-jre-alpine

# Set timezone
ENV TZ=Asia/Shanghai
ENV LOADER_PATH=/app/lib

WORKDIR /app

# Install necessary tools for healthcheck and troubleshooting
RUN apk add --no-cache tzdata bash && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone

# Copy the built Spring Boot executable JAR from builder stage
# The JAR is built to zdh_web-5.6.16-RELEASE/ directory (configured in pom.xml)
COPY --from=builder /app/zdh_web-5.6.16-RELEASE/zdh_web.jar target.jar

# Copy system-scoped dependencies (JARs from lib/ directory that aren't bundled)
COPY lib/ /app/lib/

# Copy configuration files from builder stage (contains all application properties)
COPY --from=builder /app/zdh_web-5.6.16-RELEASE/conf/ /app/conf/

# Expose application port
EXPOSE 8081

# Environment variable (required by application)
ENV ZDH_RUN_MODE=prod

# Health check - will be overridden by docker-compose healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=5 \
    CMD ss -tlnp | grep -q ':8081' || exit 1

# Run the application with proper JVM options
# LOADER_PATH env var tells PropertiesLauncher where to find additional JARs
CMD ["java", "-Xms512m", "-Xmx1024m", "-Dfile.encoding=UTF-8", "-Dspring.config.location=/app/conf/", "-Dloader.path=/app/lib,/app/conf/", "-jar", "/app/target.jar", "--spring.profiles.active=prod"]