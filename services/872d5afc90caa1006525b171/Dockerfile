# Stage 1: Builder
FROM gradle:8.10-jdk17 AS builder

WORKDIR /build

# Copy build configuration files
COPY demo-app/build.gradle demo-app/settings.gradle ./
COPY demo-app/src ./src

# Build the application
RUN gradle bootJar --no-daemon -x test

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

# Install wget for healthcheck
RUN apk add --no-cache wget

WORKDIR /home/ubuntu/deploy-projects/872d5afc90caa1006525b171

# Copy the built JAR from builder stage
COPY --from=builder /build/build/libs/*.jar app.jar

# Expose port
EXPOSE 8080

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]