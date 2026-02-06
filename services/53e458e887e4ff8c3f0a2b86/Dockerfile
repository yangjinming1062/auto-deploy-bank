# Stage 1: Build
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy entire project structure first
COPY . .

# Build and repackage the Spring Boot studio module (skip tests for container build)
RUN mvn clean package -DskipTests -B -pl studio/springboot -am

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install curl for healthcheck
RUN apk add --no-cache curl

# Copy the built JAR from builder stage (named target.jar for security scanning)
COPY --from=builder /build/studio/springboot/target/*.jar target.jar

# Expose port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "target.jar"]