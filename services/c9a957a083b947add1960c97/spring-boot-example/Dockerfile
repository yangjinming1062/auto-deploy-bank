# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage (rename to app.jar for volume mounting)
COPY --from=builder /app/target/*.jar app.jar

# Expose the application port
EXPOSE 8082

# Run the application
CMD ["java", "-jar", "app.jar"]