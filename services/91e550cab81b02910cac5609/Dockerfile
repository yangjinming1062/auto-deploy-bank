# Stage 1: Build with Gradle
FROM eclipse-temurin:17-jdk-alpine AS builder

WORKDIR /app

# Copy gradle configuration files first for better caching
COPY gradlew gradlew ./
COPY gradle/wrapper/ ./gradle/wrapper/
COPY build.gradle build.gradle
COPY settings.gradle settings.gradle
COPY gradle.properties gradle.properties
COPY defaultEnvironment.gradle defaultEnvironment.gradle

# Copy source code
COPY flashback-admin/ ./flashback-admin/
COPY flashback-core-impl/ ./flashback-core-impl/
COPY flashback-netty/ ./flashback-netty/
COPY flashback-smartproxy/ ./flashback-smartproxy/
COPY flashback-test-util/ ./flashback-test-util/
COPY mitm/ ./mitm/
COPY LICENSE ./
COPY NOTICE ./

# Download dependencies and build
RUN chmod +x ./gradlew
RUN ./gradlew :flashback-admin:shadowJar --no-daemon

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy the fat JAR from builder stage and rename to target.jar for security scanner
COPY --from=builder /app/flashback-admin/build/libs/flashback-admin-*.jar ./target.jar

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose default ports (8080 for admin API, 5555 for proxy - internal only)
EXPOSE 8080

# Health check - Rest.li server returns 200 on root path when started
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ || exit 1

# Run the application
CMD ["java", "-jar", "target.jar", "-port", "8080", "-packages", "com.linkedin.flashback"]