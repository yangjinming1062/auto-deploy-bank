# Multi-stage build for Event-Sourcing + CQRS Banking Application
# This builds the API Gateway Service as the main entry point

# Stage 1: Builder
FROM eclipse-temurin:8-jdk AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y wget unzip && rm -rf /var/lib/apt/lists/*
RUN wget -q https://services.gradle.org/distributions/gradle-4.10.3-bin.zip && \
    unzip -q gradle-4.10.3-bin.zip && rm gradle-4.10.3-bin.zip
ENV PATH=$PATH:/app/gradle-4.10.3/bin

# Copy build files first for better caching
COPY java-spring/settings.gradle java-spring/gradle.properties ./
COPY java-spring/buildSrc ./buildSrc
RUN cat > build.gradle << 'EOFBUILD'
buildscript {
    repositories {
        maven { url 'https://repo.spring.io/release' }
        mavenCentral()
    }
    dependencies {
        classpath("org.springframework.boot:spring-boot-gradle-plugin:1.3.5.RELEASE")
    }
}

allprojects {
    group = "net.chrisrichardson.eventstore"
}

task wrapper(type: Wrapper) {
    gradleVersion = '2.0'
}

subprojects {
    apply plugin: 'java'
    sourceCompatibility = 1.8
    targetCompatibility = 1.8

    repositories {
        maven { url 'https://repo.spring.io/release' }
        mavenCentral()
        jcenter()
    }
}
EOFBUILD

# Copy source files
COPY java-spring/api-gateway-service/src ./src
COPY java-spring/common-backend ./common-backend
COPY java-spring/common-swagger ./common-swagger
COPY java-spring/buildSrc ./buildSrc

# Build the API Gateway service
RUN gradle :api-gateway-service:clean :api-gateway-service:build -x test --no-daemon

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# Create non-root user for security
RUN addgroup -S app && adduser -S app -G app
USER app

# Copy the built JAR from builder stage
COPY --from=builder /app/api-gateway-service/build/libs/*.jar app.jar

# Expose the internal port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

# Start the application
CMD ["java", "-jar", "app.jar"]