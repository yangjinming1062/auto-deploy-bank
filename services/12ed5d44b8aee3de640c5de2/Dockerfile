#
# Root Dockerfile - Build Conductor Server
# Multi-stage build for Conductor server JAR
#

# ===========================================================================================================
# Builder stage - Build the Conductor server JAR
# ===========================================================================================================
FROM azul/zulu-openjdk-debian:17 AS builder

LABEL maintainer="Conductor OSS"

WORKDIR /conductor

# Copy the project
COPY . /conductor

# Build the server JAR (exclude tests for faster build)
RUN ./gradlew :conductor-server:build -x test -x spotlessCheck

# ===========================================================================================================
# Final stage - Runtime image
# ===========================================================================================================
FROM alpine:3.19

# Install OpenJDK 17
RUN apk add openjdk17
RUN apk add curl

WORKDIR /app

# Copy config files
COPY docker/server/config /app/config

# Copy the built JAR to both locations for compatibility
COPY --from=builder /conductor/server/build/libs/conductor-server-boot.jar /app/target.jar
COPY --from=builder /conductor/server/build/libs/conductor-server-boot.jar /app/app.jar

# The container will run with java -jar, suitable for docker-compose
CMD ["java", "-jar", "/app/target.jar"]
