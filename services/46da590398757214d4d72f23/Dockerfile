# Multi-stage build for Spring Boot application

# Stage 1: Build stage with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy parent pom.xml and all module poms first
COPY pom.xml .
COPY ruoyi-admin/pom.xml ./ruoyi-admin/pom.xml
COPY ruoyi-admin/src ./ruoyi-admin/src
COPY ruoyi-common ./ruoyi-common
COPY ruoyi-modules ./ruoyi-modules
COPY ruoyi-modules-api ./ruoyi-modules-api
COPY ruoyi-extend ./ruoyi-extend

# Build the application
RUN mvn clean package -Pprod -DskipTests -B

# Stage 2: Runtime stage with JRE
FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app

# Copy JAR from builder stage and rename to app.jar
COPY --from=builder /app/ruoyi-admin/target/*.jar app.jar

# Create directory for logs
RUN mkdir -p /app/logs

# Expose the port the app runs on
EXPOSE 6039

# Run the application
CMD ["java", "-jar", "app.jar"]