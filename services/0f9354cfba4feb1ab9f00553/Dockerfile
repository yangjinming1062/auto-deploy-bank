# Multi-stage build for Spring Boot application
# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy entire API directory
COPY api .

# Install parent and base-common module first (resolves local dependencies)
RUN mvn install -pl jeecg-boot-base-common -am -Dmaven.test.skip=true -B

# Download Lombok for delombok processing
RUN curl -sL https://projectlombok.org/downloads/lombok.jar -o /tmp/lombok.jar && \
    mkdir -p /tmp/delombok && \
    java -jar /tmp/lombok.jar delombok \
        -d /tmp/delombok \
        jeecg-boot-module-system/src/main/java

# Backup original sources and replace with delomboked sources
RUN mv jeecg-boot-module-system/src/main/java jeecg-boot-module-system/src/main/java.orig && \
    cp -r /tmp/delombok jeecg-boot-module-system/src/main/java

# Build with delomboked sources (no Lombok annotations needed)
RUN mvn clean package -pl jeecg-boot-module-system -Dmaven.test.skip=true -B

# Stage 2: Create runtime image
FROM eclipse-temurin:17-jre-alpine

# Create app directory
WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/jeecg-boot-module-system/target/*.jar app.jar

# Expose port
EXPOSE 8081

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8081/api/actuator/health || exit 1

# Run the application
CMD ["java", "-jar", "app.jar"]