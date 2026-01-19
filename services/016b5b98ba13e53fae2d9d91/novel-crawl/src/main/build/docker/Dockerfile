# Multi-stage build for novel-crawl
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /build

# Copy parent pom.xml and ALL module directories (required for dependency resolution)
COPY pom.xml .
COPY novel-common novel-common
COPY novel-front novel-front
COPY novel-admin novel-admin
COPY novel-crawl novel-crawl

# Copy configuration files
COPY config config
COPY doc doc
COPY templates templates

# Download dependencies first (for better layer caching)
RUN mvn dependency:go-offline -B

# Build the novel-crawl module
RUN mvn clean package -pl novel-crawl -am -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Copy built JAR from builder stage
COPY --from=builder /build/novel-crawl/target/novel-crawl-*.jar app.jar

# Copy configuration files
COPY --from=builder /build/novel-crawl/target/classes /app/classes

# Expose port
EXPOSE 8081

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8081/actuator/health || exit 1

# Start the application
CMD ["java", "-jar", "app.jar"]