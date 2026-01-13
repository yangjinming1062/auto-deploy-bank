# Multi-stage build for Spring Boot application
# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy pom.xml and download dependencies
COPY 3_api_platform/api-platform/pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY 3_api_platform/api-platform/src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:8-jre

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/target/*.jar app.jar

# Expose the application port
EXPOSE 8089

# Run the application
CMD ["java", "-jar", "app.jar"]