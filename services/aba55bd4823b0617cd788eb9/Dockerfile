# Stage 1: Builder stage using Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY 07-spring-boot-spring-mvc-crud/01-thymeleaf-demo-employees-list/pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY 07-spring-boot-spring-mvc-crud/01-thymeleaf-demo-employees-list/src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/target/*.jar app.jar

# Also copy to target.jar for volume mounting and security scanning
RUN cp app.jar target.jar

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]