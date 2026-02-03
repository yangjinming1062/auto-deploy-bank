# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /app

# Copy entire project for multi-module build
COPY . .

# Install parent POM first and build gms-server module
RUN mvn install -N -B && \
    cd gms-server && \
    mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:21-jre-alpine

# Install netcat for health check
RUN apk add --no-cache netcat-openbsd

WORKDIR /app

# Create non-root user for security
RUN addgroup -S app && adduser -S app -G app

# Copy the built JAR from builder stage to target.jar (for volume mount scanning)
COPY --from=builder /app/gms-server/target/BeiDou.jar target.jar

# Copy WZ game resource files, scripts and resources
COPY --from=builder /app/gms-server/wz wz
COPY --from=builder /app/gms-server/wz-zh-CN wz-zh-CN
COPY --from=builder /app/gms-server/scripts scripts
COPY --from=builder /app/gms-server/scripts-zh-CN scripts-zh-CN
COPY --from=builder /app/gms-server/src/main/resources main/resources

# Copy frontend static files (Vue.js build)
COPY --from=builder /app/gms-ui/dist main/resources/static

# Change ownership to non-root user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose application ports
# 8686 - Main HTTP port (Spring Boot)
# 8484 - Login port (Netty-based game client connections)
EXPOSE 8686 8484

# Health check using TCP port check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD nc -z localhost 8686 || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "target.jar"]