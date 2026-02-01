# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application (skip tests for docker build)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create logs directory
RUN mkdir -p logs

# Copy the built JAR from builder stage
COPY --from=builder /app/target/ckibana-1.0.0-SNAPSHOT.jar target.jar

# Expose application port
EXPOSE 8080

# Set environment variables
ENV JAVA_OPTS="-Xmx1g -XX:MaxRAMPercentage=75 -XX:InitialRAMPercentage=75 -XX:+UseG1GC -XX:G1HeapRegionSize=16m"

# Run the application
CMD ["java", "-jar", "-Dspring.profiles.active=default", "target.jar"]