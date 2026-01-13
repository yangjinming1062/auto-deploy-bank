# Multi-stage Docker build for Armeria annotated-http-service example

# Stage 1: Build stage
FROM eclipse-temurin:17-jdk-alpine AS builder

# Set working directory
WORKDIR /build

# Copy Gradle wrapper and build files
COPY gradlew .
COPY gradle gradle
COPY gradle.properties .
COPY build.gradle .
COPY settings.gradle .
COPY dependencies.toml .

# Copy all required modules for the build
COPY core core
COPY annotation-processor annotation-processor
COPY examples examples
COPY spring spring
COPY brave brave
COPY jetty jetty
COPY logback logback
COPY scalapb scalapb
COPY scala scala
COPY thrift thrift
COPY tomcat tomcat
COPY xds xds
COPY testing-internal testing-internal
COPY site site
COPY docs-client docs-client
COPY benchmarks benchmarks
COPY it it
COPY ai ai
COPY athenz athenz
COPY consul consul
COPY brave brave5
COPY brave brave6
COPY bucket4j bucket4j
COPY dropwizard2 dropwizard2
COPY eureka eureka
COPY grpc grpc
COPY graphql graphql
COPY graphql-protocol graphql-protocol
COPY grpc-kotlin grpc-kotlin
COPY grpc-protocol grpc-protocol
COPY javadoc javadoc
COPY junit4 junit4
COPY junit5 junit5
COPY jsonrpc jsonrpc
COPY kafka kafka
COPY kotlin kotlin
COPY kubernetes kubernetes
COPY micrometer-context micrometer-context
COPY native-image-config native-image-config
COPY oauth2 oauth2
COPY prometheus1 prometheus1
COPY protobuf protobuf
COPY reactor3 reactor3
COPY resilience4j2 resilience4j2
COPY resteasy resteasy
COPY retrofit2 retrofit2
COPY rxjava2 rxjava2
COPY rxjava3 rxjava3
COPY saml saml
COPY sangria sangria
COPY zookeeper3 zookeeper3
COPY nacos nacos
COPY bom bom
COPY version-catalog version-catalog

# Make gradlew executable
RUN chmod +x gradlew

# Build the application
RUN ./gradlew :examples:annotated-http-service:build --no-daemon

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

# Install wget for health checks
RUN apk add --no-cache wget

# Set working directory
WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /build/examples/annotated-http-service/build/libs/*.jar app.jar

# Expose the internal port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/docs || exit 1

# Run the application
CMD ["java", "-jar", "app.jar"]