# Multi-stage build for Gradle-based Spring Boot application
# Stage 1: Builder
FROM gradle:8.5-jdk17 AS builder

WORKDIR /app

# Create minimal build.gradle for Docker build
RUN cat > build.gradle << 'EOFBUILD'
buildscript {
    repositories {
        mavenCentral()
    }
    dependencies {
        classpath "org.springframework.boot:spring-boot-gradle-plugin:2.7.18"
    }
}

plugins {
    id 'java'
    id 'org.springframework.boot' version '2.7.18'
}

group = 'jp.classmethod.aws.gradle.sample'
version = '0.1-SNAPSHOT'
ext.artifactId = '05-beanstalk'

repositories {
    mavenCentral()
}

dependencies {
    implementation "org.springframework.boot:spring-boot-starter-actuator:2.7.18"
    implementation "org.springframework.boot:spring-boot-starter-web:2.7.18"
}

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}

tasks.named('bootJar') {
    archiveFileName = 'target.jar'
}
EOFBUILD

# Copy source files from samples/05-beanstalk
COPY samples/05-beanstalk/src/main/resources ./src/main/resources
COPY samples/05-beanstalk/src/main/java ./src/main/java

# Build the JAR as target.jar for security scanning
RUN gradle clean bootJar -x test --no-daemon

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Install wget for healthcheck
RUN apk add --no-cache wget

# Copy built JAR (named target.jar for security scanning)
COPY --from=builder /app/build/libs/target.jar app.jar
# Also keep target.jar in root for volume mount
COPY --from=builder /app/build/libs/target.jar target.jar

# Set ownership
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ || exit 1

# Run application
ENTRYPOINT ["java", "-jar", "app.jar"]