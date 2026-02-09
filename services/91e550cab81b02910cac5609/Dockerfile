# Stage 1: Builder
FROM gradle:7.6-jdk17 AS builder

WORKDIR /app

# Copy build configuration files first for better caching
COPY build.gradle settings.gradle ./
COPY gradle.properties ./
COPY gradle ./gradle
COPY gradlew ./

# Copy source code
COPY flashback-admin ./flashback-admin
COPY flashback-core-impl ./flashback-core-impl
COPY flashback-netty ./flashback-netty
COPY flashback-smartproxy ./flashback-smartproxy
COPY flashback-test-util ./flashback-test-util
COPY mitm ./mitm
COPY LICENSE ./
COPY NOTICE ./

# Build the shadow jar (fat jar) for flashback-admin
RUN gradle :flashback-admin:shadowJar --no-daemon -x test

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy the built jar from builder stage
# Rename to target.jar for security scanner volume mount
COPY --from=builder /app/flashback-admin/build/libs/flashback-admin*.jar /app/target.jar

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose the admin server port (default 8080)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

# Run the application - specify port 8080 explicitly
CMD ["java", "-jar", "target.jar", "-port", "8080", "-packages", "com.linkedin.flashback"]