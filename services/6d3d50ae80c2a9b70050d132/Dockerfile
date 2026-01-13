# Multi-stage build for Spring Boot application
# Stage 1: Build the application with Java 8
FROM maven:3.8.6-openjdk-8-slim AS builder

WORKDIR /app

# Copy pom.xml and download dependencies
COPY springboot-jasypt/pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY springboot-jasypt/src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image with Java 17
FROM eclipse-temurin:17-jre

WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/target/*.jar app.jar

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]