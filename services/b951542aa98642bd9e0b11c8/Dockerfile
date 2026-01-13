# Multi-stage build for Java/Spring Boot application

# Stage 1: Build the application
FROM gradle:7.6-jdk8 AS builder

WORKDIR /app

# Copy gradle files
COPY build.gradle /app/
COPY settings.gradle /app/
COPY gradle/wrapper/ /app/gradle/wrapper/
COPY gradlew /app/gradlew
COPY gradlew.bat /app/gradlew.bat

# Copy source code
COPY application/ /app/application/
COPY acceptance-tests/ /app/acceptance-tests/
COPY integration-tests/ /app/integration-tests/

# Make gradlew executable
RUN chmod +x /app/gradlew

# Build the application
RUN ./gradlew clean build -x test

# Stage 2: Runtime stage
FROM eclipse-temurin:8-jre-alpine

WORKDIR /app

# Create directories
RUN mkdir -p /app/output /app/runtime

# Copy JAR from builder stage
# Copy to /app/output/target.jar for volume mount (extraction to host)
# Copy to /app/runtime/target.jar for running (protected from volume mount)
COPY --from=builder /app/application/build/clean-architecture-example.jar /app/output/target.jar
COPY --from=builder /app/application/build/clean-architecture-example.jar /app/runtime/target.jar

# Create a startup script to ensure JAR is at mount point
RUN echo '#!/bin/sh' > /app/startup.sh && \
    echo 'cp /app/runtime/target.jar /app/target.jar' >> /app/startup.sh && \
    echo 'java -jar /app/runtime/target.jar' >> /app/startup.sh && \
    chmod +x /app/startup.sh

# Expose port
EXPOSE 8080

# Run startup script which copies JAR to mount point and then runs the application
CMD ["/app/startup.sh"]