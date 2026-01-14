# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY . .

# Build the project
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# Install required packages
RUN apk add --no-cache curl tzdata fontconfig ttf-dejavu

# Set timezone
ENV TZ=Asia/Shanghai

WORKDIR /application

# Copy the built JAR from builder stage
COPY --from=builder /app/tduck-api/target/tduck-api-*.jar app.jar

# Create upload directory for file uploads
RUN mkdir -p /application/BOOT-INF/lib/upload

# Expose application port
EXPOSE 8999

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8999/actuator/health || exit 1

# Run Spring Boot application
ENTRYPOINT ["java", "-jar", "app.jar"]