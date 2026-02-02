# Stage 1: Build stage using Maven and Eclipse Temurin 17
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching (from demo subdirectory)
COPY demo/pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY demo/src ./src

# Build the project (skip tests for faster build)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage using Eclipse Temurin 17 JRE Alpine
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built WAR (Spring Boot executable WAR) from builder stage
# The WAR file is renamed to target.jar for security scanning consistency
COPY --from=builder /app/target/*.war target.jar

# Expose the application port (configured as 9090 in application.properties)
EXPOSE 9090

# Run the application (Spring Boot WAR files are executable)
CMD ["java", "-jar", "target.jar"]