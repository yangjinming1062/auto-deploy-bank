# Stage 1: Build stage with Java 8
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy entire project for multi-module Maven build
COPY . .

# Build the project and copy JAR to a known location for extraction
RUN mvn clean package -DskipTests -B && \
    cp powerjob-server/powerjob-server-starter/target/powerjob-server-starter-*.jar /app-target.jar

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Set timezone
ENV TZ=Asia/Shanghai

# Create non-root user for security
RUN addgroup -g 1000 app && adduser -u 1000 -G app -s /bin/sh -D app

# Copy the JAR from builder stage to target.jar (for volume mount/security scanning)
COPY --from=builder /app-target.jar /app/target.jar

# Change ownership to non-root user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose ports: HTTP (7700), Akka (10086), HTTP transporter (10010)
EXPOSE 7700 10086 10010

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:7700/actuator/health || exit 1

# Start the application
CMD ["java", "-Xmx512m", "-jar", "target.jar"]