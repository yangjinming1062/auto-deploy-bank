# Multi-stage build for Spring Initializr service
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17-alpine AS builder

# Set working directory
WORKDIR /build

# Copy pom.xml first to leverage Docker cache
COPY pom.xml .
COPY initializr-parent/pom.xml initializr-parent/
COPY initializr-bom/pom.xml initializr-bom/
COPY initializr-generator/pom.xml initializr-generator/
COPY initializr-generator-spring/pom.xml initializr-generator-spring/
COPY initializr-generator-test/pom.xml initializr-generator-test/
COPY initializr-metadata/pom.xml initializr-metadata/
COPY initializr-web/pom.xml initializr-web/
COPY initializr-actuator/pom.xml initializr-actuator/
COPY initializr-version-resolver/pom.xml initializr-version-resolver/
COPY initializr-docs/pom.xml initializr-docs/
COPY initializr-service-sample/pom.xml initializr-service-sample/

# Copy source code first
COPY . .

# Build all modules first (without repackage) and install to local repo
RUN mvn clean install -DskipTests -B

# Repackage only the sample service module to create executable JAR
# Must use 'package' phase for the specific module since repackage needs the original JAR
RUN mvn package spring-boot:repackage -pl initializr-service-sample -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# Create app directory
WORKDIR /app

# Copy and rename JAR from builder stage for security scanning
# Note: The repackaged JAR (without .original suffix) contains all dependencies
COPY --from=builder /build/initializr-service-sample/target/initializr-service-sample-0.22.1-SNAPSHOT.jar /app/target.jar

# Expose port 8080
EXPOSE 8080

# Health check - use basic TCP check since actuator is not included in sample
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ || exit 1

# Run the application
CMD ["java", "-jar", "target.jar"]