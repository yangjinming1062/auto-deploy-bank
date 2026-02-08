# Stage 1: Copy pre-built JAR
FROM eclipse-temurin:17-jdk-alpine AS builder

WORKDIR /build

# Copy the pre-built JAR file
COPY demo-app/build/libs/app.jar target.jar

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create non-root user for security
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

# Copy the built JAR to target.jar for volume mount
COPY --from=builder --chown=spring:spring /build/target.jar target.jar

# Expose the application port
EXPOSE 8080

# Run the application
ENTRYPOINT ["java", "-jar", "target.jar"]