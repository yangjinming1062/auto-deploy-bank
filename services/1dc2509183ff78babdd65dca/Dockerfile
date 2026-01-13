# Multi-stage build for Spring Boot application
# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml and download dependencies
COPY forest-examples/example-springboot/pom.xml /app/
RUN mvn dependency:go-offline -B -f /app/pom.xml

# Copy source code
COPY forest-examples/example-springboot/src /app/src

# Build the application
RUN mvn clean package -DskipTests -B -f /app/pom.xml

# Stage 2: Create runtime image
FROM eclipse-temurin:17-jre-alpine AS runtime

WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/target/*.jar app.jar
# Also copy JAR to target.jar for volume extraction
COPY --from=builder /app/target/*.jar target.jar

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]