# Multi-stage build for Spring Boot application
# Stage 1: Builder with Maven and Java 8 (project requires Java 8)
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /build

# Copy dependencies from local directory
COPY fangjia-common fangjia-common
COPY fangjia-api-client fangjia-api-client
COPY pom.xml .
COPY src ./src

# Build dependencies first
WORKDIR /build/fangjia-common
RUN mvn clean install -DskipTests

WORKDIR /build/fangjia-api-client
RUN mvn clean install -DskipTests

# Build the main application
WORKDIR /build
RUN mvn clean package -DskipTests

# Stage 2: Runtime with JRE
FROM eclipse-temurin:8-jre-alpine

WORKDIR /app

# Copy JAR from builder stage
# Named as target.jar for volume mount security scanning
COPY --from=builder /build/target/fangjia-fsh-api-1.0.jar target.jar

# Expose the internal port (Spring Boot application port)
EXPOSE 8080

# Health check using wget to check if port is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ || exit 1

# Start the application
CMD ["java", "-jar", "target.jar"]