# Stage 1: Build the application with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml and download dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Create runtime image
FROM eclipse-temurin:17-jdk

WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/target/lab-72-minio-*.jar app.jar

# Expose port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]