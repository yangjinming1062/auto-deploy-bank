# Multi-stage build for HAPI FHIR Spring Boot Server

# Stage 1: Build the JAR
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy entire source code
COPY . .

# Build the specific module to get dependencies
# First build hapi-fhir-jpa and all dependencies needed by the sample server
# Skip buildnumber plugin which requires git
RUN mvn clean install -DskipTests -B -P FASTINSTALL -Drevision=8.7.2-SNAPSHOT -Dmaven.buildNumber.skip=true \
    -pl hapi-fhir-jpaserver-base,hapi-fhir-spring-boot/hapi-fhir-spring-boot-autoconfigure,hapi-fhir-spring-boot/hapi-fhir-spring-boot-starter,hapi-fhir-jaxrsserver-base,hapi-fhir-validation-resources-dstu3,hapi-fhir-structures-dstu3 -am && \
    mvn package spring-boot:repackage -DskipTests -B -P FASTINSTALL -Drevision=8.7.2-SNAPSHOT -Dmaven.buildNumber.skip=true \
    -pl hapi-fhir-spring-boot/hapi-fhir-spring-boot-samples/hapi-fhir-spring-boot-sample-server-jersey

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the Spring Boot fat JAR from builder stage
# Use app.jar for execution (volume mount provides target.jar for security scanning at /scanning/)
COPY --from=builder /app/hapi-fhir-spring-boot/hapi-fhir-spring-boot-samples/hapi-fhir-spring-boot-sample-server-jersey/target/hapi-fhir-spring-boot-sample-server-jersey-8.7.2-SNAPSHOT.jar app.jar

# Verify JAR exists
RUN ls -la /app/app.jar

# Expose port 8080
EXPOSE 8080

# Health check using FHIR metadata endpoint (since actuator is disabled)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/fhir/metadata 2>/dev/null || exit 1

# Run the Spring Boot application with proper logging
CMD ["java", "-jar", "-Dspring.profiles.active=default", "-Dlogging.level.root=INFO", "app.jar"]