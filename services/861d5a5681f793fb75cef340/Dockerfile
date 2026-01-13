# Multi-stage build for Redis Manager
# Stage 1: Build frontend and backend
FROM maven:3.9-eclipse-temurin-17 AS builder

# Install Node.js and npm for frontend build
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy pom.xml and download dependencies
COPY redis-manager-dashboard/pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY redis-manager-dashboard ./redis-manager-dashboard
COPY redis-manager-ui/redis-manager-vue/package*.json ./redis-manager-ui/redis-manager-vue/
COPY redis-manager-ui/redis-manager-vue/ ./redis-manager-ui/redis-manager-vue/

# Build frontend
WORKDIR /build/redis-manager-ui/redis-manager-vue
RUN npm install --legacy-peer-deps && npm run build

# Move frontend build to backend static resources
WORKDIR /build
# Create directories if they don't exist
RUN mkdir -p redis-manager-dashboard/src/main/resources/static && \
    mkdir -p redis-manager-dashboard/src/main/resources/templates && \
    cp -r redis-manager-ui/redis-manager-vue/dist/* redis-manager-dashboard/src/main/resources/static/ 2>/dev/null || echo "No static files to copy" && \
    cp redis-manager-ui/redis-manager-vue/dist/index.html redis-manager-dashboard/src/main/resources/templates/ 2>/dev/null || echo "No index.html to copy"

# Build backend JAR and extract tar.gz to create fat JAR
WORKDIR /build/redis-manager-dashboard
# Build with assembly (default descriptor)
RUN mvn clean package -DskipTests -B && ls -lh target/*.jar && ls -lh target/*.tar.gz

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# Install netcat, zip utilities, and openjdk for jar command
RUN apk add --no-cache netcat-openbsd zip unzip openjdk17-jdk

WORKDIR /app

# Copy original JAR and lib directory
# Note: JAR must be at /app/target.jar for security scanning
COPY --from=builder /build/redis-manager-dashboard/target/redis-manager-dashboard-2.3.3-RELEASE.jar /app/target.jar
COPY --from=builder /build/redis-manager-dashboard/target/redis-manager-dashboard-2.3.3-RELEASE.tar.gz /tmp/app.tar.gz

# Extract lib directory and config files
RUN cd /tmp && tar -xzf app.tar.gz && rm app.tar.gz && \
    # Extract lib JARs for classpath
    mkdir -p /app/lib && \
    cp -r lib/* /app/lib/ 2>/dev/null || true && \
    # Copy config files
    mkdir -p /app/conf && \
    cp -r conf/* /app/conf/ 2>/dev/null || true && \
    # Replace placeholders in application.yml
    find /app/conf -name "application.yml" -type f -exec sed -i \
        -e "s/\${SERVER_PORT:8182}/8182/g" \
        -e "s/\${DATASOURCE_URL.*}/jdbc:mysql:\/\/mysql:3306\/redis_manager?useUnicode=true\&characterEncoding=utf-8\&serverTimezone=GMT%2B8/g" \
        -e "s/\${DATASOURCE_USERNAME:root}/root/g" \
        -e "s/\${DATASOURCE_PASSWORD.*}/redis_manager_password/g" \
        -e "s/\${DATASOURCE_DATABASE:redis_manager}/redis_manager/g" \
        -e "s/company-name: xxx/company-name: xxx/g" \
        -e "s/server: xxx/server: xxx/g" \
        -e "s/site-key: xxx/site-key: xxx/g" \
        -e "s/site-secret: xxx/site-secret: xxx/g" \
        {} + && \
    rm -rf /tmp/*

# Expose port
EXPOSE 8182

# Health check - check if port 8182 is listening
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD nc -z localhost 8182 || exit 1

# Run with classpath including lib directory and conf
# Add JVM args to support Java 17 module system for Spring Cloud Eureka
CMD java --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.lang.reflect=ALL-UNNAMED --add-opens=java.base/java.net=ALL-UNNAMED --add-opens=java.base/javax.annotation=ALL-UNNAMED --add-opens=java.base/java.text=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/sun.nio.ch=ALL-UNNAMED --add-opens=java.desktop/java.awt.font=ALL-UNNAMED -cp /app/target.jar:/app/lib/*:/app/conf com.newegg.ec.redis.RedisManagerApplication