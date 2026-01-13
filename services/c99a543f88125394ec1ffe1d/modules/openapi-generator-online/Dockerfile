# Multi-stage build for OpenAPI Generator Online
# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy Maven wrapper and pom.xml from parent directory
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .

# Copy all module POMs and source code
COPY modules/openapi-generator-core/pom.xml modules/openapi-generator-core/pom.xml
COPY modules/openapi-generator/pom.xml modules/openapi-generator/pom.xml
COPY modules/openapi-generator-cli/pom.xml modules/openapi-generator-cli/pom.xml
COPY modules/openapi-generator-maven-plugin/pom.xml modules/openapi-generator-maven-plugin/pom.xml
COPY modules/openapi-generator-gradle-plugin/pom.xml modules/openapi-generator-gradle-plugin/pom.xml
COPY modules/openapi-generator-online/pom.xml modules/openapi-generator-online/pom.xml

# Copy source code
COPY modules/openapi-generator-core/src modules/openapi-generator-core/src
COPY modules/openapi-generator/src modules/openapi-generator/src
COPY modules/openapi-generator-cli/src modules/openapi-generator-cli/src
COPY modules/openapi-generator-maven-plugin/src modules/openapi-generator-maven-plugin/src
COPY modules/openapi-generator-gradle-plugin/src modules/openapi-generator-gradle-plugin/src
COPY modules/openapi-generator-online/src modules/openapi-generator-online/src

# Make Maven wrapper executable
RUN chmod +x ./mvnw

# Clear potentially problematic environment variables
ENV MAVEN_OPTS=""
ENV MAVEN_CONFIG=""

# Build the application (using sh to avoid shell parsing issues)
RUN ["./mvnw", "clean", "package", "-DskipTests", "-B", "-pl", "modules/openapi-generator-online", "-am"]

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /build/modules/openapi-generator-online/target/openapi-generator-online.jar app.jar

# Create a symbolic link for security scanning compatibility
RUN ln -s app.jar target.jar

# GENERATOR_HOST can be used to determine the target location of a download link
# The default value assumes binding to host via: docker -p 8080:8080 image_name
ENV GENERATOR_HOST=""
ENV JAVA_OPTS="-DloggerPath=conf/log4j.properties"

EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ || exit 1

CMD ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]