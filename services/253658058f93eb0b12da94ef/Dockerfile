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

# Install wget for healthcheck
RUN apk add --no-cache wget

# Copy the built JAR from builder stage
COPY --from=builder /app/target/*.jar target.jar

# Create app.jar as the main application entry
RUN ln -s target.jar app.jar

# Copy external configuration
COPY application.yml .

# Expose the HTTP port
EXPOSE 8080

# Start the application
CMD ["java", "-jar", "target.jar"]