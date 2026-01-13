# Multi-stage build for renren-admin
# Stage 1: Build the application using Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy all module poms and source code for multi-module build
COPY pom.xml .
COPY renren-admin/pom.xml renren-admin/
COPY renren-common renren-common/
COPY renren-dynamic-datasource renren-dynamic-datasource/
COPY renren-api renren-api/
COPY renren-generator renren-generator/
COPY renren-admin/src renren-admin/src

# Build all modules first (to install dependencies), then rebuild renren-admin specifically
RUN mvn clean install -DskipTests -B

# Stage 2: Runtime image
FROM amazoncorretto:17-alpine

WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/renren-admin/target/renren-admin.jar target.jar

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=10 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/renren-admin/doc.html || exit 1

# Start the application
ENTRYPOINT ["java", "-jar", "target.jar"]