# Stage 1: Build stage
FROM maven:3.8-openjdk-8 AS builder

# Set working directory
WORKDIR /app

# Copy root pom.xml for multi-module build
COPY pom.xml .
COPY mall-common ./mall-common
COPY mall-mbg ./mall-mbg
COPY mall-security ./mall-security
COPY mall-demo ./mall-demo
COPY mall-admin ./mall-admin
COPY mall-search ./mall-search
COPY mall-portal ./mall-portal

# Build all modules to install to local repository, then build mall-admin
RUN mvn clean install -DskipTests -B && \
    cd mall-admin && mvn clean package -DskipTests -B

# Stage 2: Runtime stage
FROM eclipse-temurin:8-jre-alpine

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN addgroup -S app && adduser -S app -G app

# Create log directories for logback (required by the application)
RUN mkdir -p /var/logs/spring.log/debug /var/logs/spring.log/error && \
    chmod -R 755 /var/logs && chown -R app:app /var/logs

# Copy the built JAR from builder stage
COPY --from=builder /app/mall-admin/target/mall-admin-1.0-SNAPSHOT.jar /app/target.jar

# Change ownership to non-root user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose the application port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "-Dspring.profiles.active=prod", "/app/target.jar"]