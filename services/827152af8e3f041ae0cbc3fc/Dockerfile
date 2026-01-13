# Multi-stage build for Spring Boot application
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy the entire project
COPY springbt_uid_generator/ ./springbt_uid_generator/

# Build the entire project to install local modules
RUN cd /app/springbt_uid_generator && mvn clean install -DskipTests -B

# Build the specific uid-consumer module
RUN cd /app/springbt_uid_generator/uid-consumer && mvn clean package -DskipTests -B

# Stage 2: Runtime image with minimal JRE
FROM eclipse-temurin:8-jre-alpine

WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/springbt_uid_generator/uid-consumer/target/*.jar app.jar

# Expose port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]