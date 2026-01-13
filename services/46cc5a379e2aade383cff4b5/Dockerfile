# Multi-stage build for Spring Boot application
# Stage 1: Build the application with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml and download dependencies
COPY "【06】文件包含漏洞原理与实际案例介绍/fileInclude(springboot+thymeleaf)/pom.xml" .
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY "【06】文件包含漏洞原理与实际案例介绍/fileInclude(springboot+thymeleaf)/src" ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Create runtime image
FROM eclipse-temurin:17-jdk

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/target/*.jar app.jar

# Expose port 8080
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]