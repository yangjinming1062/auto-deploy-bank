########################################################################
# Multi-stage Dockerfile for H2O (Java application with Gradle build)
########################################################################

# Stage 1: Build stage using Maven with Java 17
FROM maven:3.9-eclipse-temurin-17 AS builder

# Install necessary build tools including Node.js for web UI
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    unzip \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /build

# Copy everything (Gradle wrapper, build files, and all source code)
COPY . .

# Make gradlew executable
RUN chmod +x gradlew

# Download dependencies and build the project (skip tests)
# Build the entire project including h2o-assemblies:main
# Include web UI build tasks now that Node.js is available
RUN ./gradlew --parallel :h2o-assemblies:main:build -x test \
    -x :h2o-assemblies:genmodel:build \
    -x :h2o-bindings:runGenerateRESTAPIBindingsSrc \
    -x :h2o-bindings:compileJava \
    -x :h2o-r:getRVersion \
    -x :h2o-r:gitbranch \
    -x :h2o-r:setProperties \
    -x :h2o-py:verifyDependencies \
    -x :h2o-py-mlflow-flavor:buildDist \
    -x :h2o-py-cloud-extensions:buildDist \
    && \
    cp /build/h2o-assemblies/main/build/libs/main.jar /build/h2o.jar

# Stage 2: Runtime stage using minimal JRE image
FROM eclipse-temurin:17-jre-alpine

# Install ca-certificates for HTTPS connections
RUN apk add --no-cache ca-certificates

# Create H2O user and group
RUN addgroup -g 1000 h2o && \
    adduser -D -u 1000 -G h2o h2o

# Set working directory
WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /build/h2o.jar /app/h2o.jar

# Switch to h2o user
USER h2o

# Expose H2O ports (54321 for API, 54322 for flow)
EXPOSE 54321 54322

# Health check to ensure service is ready
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:54321/ || exit 1

# Run H2O in foreground with 4GB heap (adjustable via environment)
CMD ["java", "-Xmx4g", "-jar", "/app/h2o.jar"]