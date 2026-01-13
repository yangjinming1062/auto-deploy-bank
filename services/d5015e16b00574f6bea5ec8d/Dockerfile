# Stage 1: Build the application using Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy pom.xml and download dependencies
COPY lab-72-minio/pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY lab-72-minio/src ./src

# Build the application
RUN mvn clean package -DskipTests -B

# Stage 2: Create the runtime image
FROM eclipse-temurin:17-jre

# Set working directory
WORKDIR /app

# Copy the JAR from builder stage to app.jar (built JAR)
COPY --from=builder /app/target/*.jar app.jar

# Create scan directory for volume mount
RUN mkdir -p /app/scan

# Expose port 8080
EXPOSE 8080

# Run the application using the built JAR
CMD ["java", "-jar", "app.jar"]