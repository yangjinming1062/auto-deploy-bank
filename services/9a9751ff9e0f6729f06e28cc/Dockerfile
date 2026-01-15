# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /app

# Copy the parent pom.xml (without module references for standalone build)
COPY pom.xml /app/pom.xml

# Copy only the demo-crud-application module
COPY demo-crud-application/pom.xml /app/demo-crud-application/pom.xml
COPY demo-crud-application/src /app/demo-crud-application/src

# Copy application configuration from root
COPY src/main/resources/application.properties /app/demo-crud-application/src/main/resources/

# Build the application (skip tests for image creation)
RUN cd /app/demo-crud-application && mvn -B clean package -DskipTests

# Stage 2: Runtime stage
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage to target.jar for security scanning
COPY --from=builder /app/demo-crud-application/target/*.jar target.jar

# Expose the application port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "target.jar"]