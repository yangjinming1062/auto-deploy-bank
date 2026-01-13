# Multi-stage build for health-check Spring Boot application
# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /build

# Copy the entire project (parent POM and all modules)
COPY . .

# Create application.properties if it doesn't exist
# Copy custom application.properties with cache configuration
COPY health-check/src/main/resources/application.properties /tmp/app.properties
RUN if [ -f /tmp/app.properties ]; then \
      mkdir -p health-check/src/main/resources && \
      cp /tmp/app.properties health-check/src/main/resources/application.properties; \
    fi

# Build only the health-check module
RUN mvn clean package -DskipTests -B -pl health-check -am

# Stage 2: Runtime stage
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /build/health-check/target/*.jar target.jar

# Expose the application port
EXPOSE 6161

# Run the application
CMD ["java", "-jar", "target.jar"]