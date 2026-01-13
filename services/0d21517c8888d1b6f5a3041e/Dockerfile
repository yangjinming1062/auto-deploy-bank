# Multi-stage build for Spring Boot application
# Stage 1: Maven builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy Maven configuration files
COPY pom.xml .
COPY ruoyi-admin/pom.xml ./ruoyi-admin/pom.xml
COPY ruoyi-common ./ruoyi-common
COPY ruoyi-extend ./ruoyi-extend
COPY ruoyi-modules ./ruoyi-modules
COPY ruoyi-modules-api ./ruoyi-modules-api

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code
COPY . .

# Build the application
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage with JRE
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install curl for healthchecks
RUN apk add --no-cache curl

# Copy the built JAR from builder stage
COPY --from=builder /build/ruoyi-admin/target/ruoyi-admin.jar target.jar

# Expose the application port
EXPOSE 6039

# Run the application
CMD ["java", "-jar", "target.jar"]
