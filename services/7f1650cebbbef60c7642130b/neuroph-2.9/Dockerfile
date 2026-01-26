# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy Core module and parent pom
COPY pom.xml ./
COPY Core ./Core

# Build only the Core module (skip tests for speed)
RUN cd /app && mvn -f Core/pom.xml clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app

# Copy the built JAR from builder
COPY --from=builder /app/Core/target/*.jar app.jar

# Expose the service port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]