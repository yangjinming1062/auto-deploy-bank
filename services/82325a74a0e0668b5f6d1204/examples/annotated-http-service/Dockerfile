# Multi-stage build for Armeria annotated HTTP service
# Stage 1: Build the application
FROM azul/zulu-openjdk:17 AS builder

# Set working directory
WORKDIR /app

# Copy project files
COPY gradle gradle
COPY gradlew .
COPY gradle.properties .
COPY settings.gradle .
COPY build.gradle .
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
COPY tomcat8 tomcat8
COPY tomcat9 tomcat9
COPY tomcat10 tomcat10
COPY xds xds
COPY xds-api xds-api
COPY xds-validator xds-validator
COPY testing-internal testing-internal
COPY site site
COPY docs-client docs-client
COPY benchmarks benchmarks
COPY it it
COPY ai ai
COPY athenz athenz
COPY consul consul
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

# Copy example source and build files
COPY examples/annotated-http-service/src src
COPY examples/annotated-http-service/build.gradle build.gradle.example

# Make Gradle wrapper executable
RUN chmod +x gradlew

# Build the specific example module
# Disable ErrorProne for Java 17 compatibility
# Use installDist to create distribution with all dependencies
RUN ./gradlew :examples:annotated-http-service:installDist --no-daemon -x test -PnoLint

# Stage 2: Runtime image
FROM azul/zulu-openjdk:17

# Install wget for health checks
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the built distribution from builder stage
# installDist creates a distribution with all dependencies
COPY --from=builder /app/examples/annotated-http-service/build/install/annotated-http-service/. /app/
# Also copy JAR for extraction - use specific JAR file
COPY --from=builder /app/examples/annotated-http-service/build/libs/armeria-examples-annotated-http-service-1.34.2-SNAPSHOT.jar target.jar

# Create a non-root user for security
RUN addgroup --gid 1001 armeria && \
    adduser --uid 1001 --gid 1001 --shell /bin/false --disabled-password --gecos "" armeria && \
    chown -R armeria:armeria /app

USER armeria

# Expose the service port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/docs || exit 1

# Run the application
CMD ["/app/bin/annotated-http-service"]