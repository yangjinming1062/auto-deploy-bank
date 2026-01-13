# Stage 1: Build the application with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml (using lab-72-minio as it's the active module)
COPY lab-72-minio/pom.xml ./lab-72-minio/
WORKDIR /app/lab-72-minio

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY lab-72-minio/src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Create runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy JAR from builder stage and rename to target.jar for volume mount
COPY --from=builder /app/lab-72-minio/target/*.jar /app/target.jar

# Expose port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "/app/target.jar"]