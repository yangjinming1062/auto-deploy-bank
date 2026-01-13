# Multi-stage build for Abixen Platform Core Service
# Stage 1: Builder
FROM maven:3.8-eclipse-temurin-8 AS builder

# Copy the entire project from parent context
WORKDIR /build

# Copy parent pom.xml, configuration files, and all submodules
COPY pom.xml .
COPY checkstyle.xml .
COPY abixen-platform-common ./abixen-platform-common
COPY abixen-platform-core ./abixen-platform-core
COPY demo-data ./demo-data

# Install the common module first
WORKDIR /build/abixen-platform-common
RUN mvn install -DskipTests -B

# Build the core module
WORKDIR /build/abixen-platform-core
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:8-jre

WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /build/abixen-platform-core/target/*.jar app.war

# Expose port 8080
EXPOSE 8080

# Set the entrypoint
ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", "-Dspring.profiles.active=docker", "-jar", "app.war"]