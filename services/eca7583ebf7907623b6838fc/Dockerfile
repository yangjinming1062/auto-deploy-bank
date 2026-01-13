# Multi-stage build for Redis Manager
# Stage 1: Build frontend (Vue.js)
FROM node:18-alpine as frontend-build
WORKDIR /app/frontend
COPY redis-manager-ui/redis-manager-vue/package*.json ./
RUN npm install --legacy-peer-deps
COPY redis-manager-ui/redis-manager-vue/ ./
RUN npm run build --legacy-peer-deps

# Stage 2: Build backend (Java/Spring Boot)
FROM maven:3.9-eclipse-temurin-8 as builder
WORKDIR /app

# Copy pom.xml and download dependencies
COPY redis-manager-dashboard/pom.xml ./
COPY redis-manager-dashboard/assembly.xml ./
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY redis-manager-dashboard/src ./src
COPY --from=frontend-build /app/frontend/dist ./src/main/resources/static
COPY redis-manager-dashboard/src/main/resources/application.yml ./src/main/resources/

# Build the JAR (skip tests)
RUN mvn clean package -DskipTests -B

# Stage 3: Runtime image
FROM eclipse-temurin:8-jdk

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy JAR file and dependencies from builder stage
COPY --from=builder /app/target/redis-manager-dashboard-2.3.3-RELEASE.jar app.jar
# Copy to target.jar for security scanning volume mount
COPY --from=builder /app/target/redis-manager-dashboard-2.3.3-RELEASE.jar target.jar
COPY --from=builder /app/target/lib ./lib
COPY --from=builder /app/src/main/resources/static ./static
COPY --from=builder /app/src/main/resources/templates ./templates
COPY --from=builder /app/src/main/resources/application.yml ./application.yml
COPY --from=builder /app/src/main/resources/log4j2.xml ./log4j2.xml

# Copy bin directory
COPY bin ./bin

# Expose the application port
EXPOSE 8182

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8182/ || exit 1

# Run the application using the same approach as start.sh
CMD ["sh", "-c", "CLASSPATH=.:conf/ && for i in lib/*.jar; do CLASSPATH=${CLASSPATH}:$i; done && for i in *.jar; do CLASSPATH=${CLASSPATH}:$i; done && java -cp ${CLASSPATH} com.newegg.ec.redis.RedisManagerApplication"]