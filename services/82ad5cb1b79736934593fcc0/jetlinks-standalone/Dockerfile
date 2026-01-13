# Multi-stage build for JetLinks
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17-alpine AS builder

WORKDIR /app

# Copy all POM files needed for multi-module project
COPY pom.xml ./
COPY jetlinks-components ./jetlinks-components
COPY jetlinks-manager ./jetlinks-manager
COPY jetlinks-standalone/pom.xml ./jetlinks-standalone/pom.xml

# Install parent POM to local repository
RUN mvn -N install -B

# Copy source code
COPY jetlinks-standalone/src ./jetlinks-standalone/src

# Build the project from parent to include all modules
# Skip dependency:go-offline and build directly
RUN mvn clean package -B -DskipTests -Dmaven.test.skip=true -am -pl jetlinks-standalone

# Verify JAR was built and contains Spring Boot loader
RUN ls -lh /app/jetlinks-standalone/target/*.jar && \
    unzip -l /app/jetlinks-standalone/target/*.jar | grep -E "(JarLauncher|BOOT-INF)" || echo "Warning: JAR may not be properly repackaged"

# Stage 2: Runtime image
FROM openjdk:8u272-jdk

WORKDIR /app

# Copy built JAR from builder stage
COPY --from=builder /app/jetlinks-standalone/target/*.jar app.jar

# Rename to target.jar for security scanning
RUN mv app.jar target.jar

# Copy entrypoint script
COPY jetlinks-standalone/docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh

# Expose the application port
EXPOSE 8848

# Run the application
ENTRYPOINT ["./docker-entrypoint.sh"]