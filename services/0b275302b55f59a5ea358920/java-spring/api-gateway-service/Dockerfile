# Multi-stage build for API Gateway Service
FROM eclipse-temurin:8-jdk AS builder
WORKDIR /project
RUN apt-get update && apt-get install -y wget unzip && rm -rf /var/lib/apt/lists/*
# Install Gradle 2.14.1 - compatible with Spring Boot 1.3.5 and Java 8
RUN wget -q https://services.gradle.org/distributions/gradle-2.14.1-bin.zip && \
    unzip -q gradle-2.14.1-bin.zip && rm gradle-2.14.1-bin.zip
ENV PATH=$PATH:/project/gradle-2.14.1/bin
# Copy entire project
COPY . .
# Build
RUN gradle :api-gateway-service:assemble --no-daemon

FROM eclipse-temurin:8-jre-alpine
WORKDIR /app
# Create target directory for security scanning volume mount
RUN mkdir -p /app/target
# Copy built JAR to target directory (will be mounted from host at runtime)
COPY --from=builder /project/api-gateway-service/build/libs/*.jar /app/target/target.jar
# Also create app.jar for running
RUN cp /app/target/target.jar /app/app.jar
# Add non-root user
RUN addgroup -S app && adduser -S app -G app
USER app
EXPOSE 8080
# Volume mount point for security scanning - mount host target.jar here at runtime
VOLUME ["/app/target"]
CMD ["java", "-jar", "app.jar"]