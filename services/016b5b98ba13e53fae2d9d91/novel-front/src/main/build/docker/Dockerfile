# Multi-stage build for novel-front
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml and download dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src
COPY ../../pom.xml ./../pom.xml
COPY ../../novel-common ./../novel-common

# Build the application
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin-17-jre-alpine

WORKDIR /app

# Copy built JAR from builder stage
COPY --from=builder /app/target/novel-front-*.jar app.jar

# Copy configuration files
COPY --from=builder /app/target/classes/application*.yml ./application.yml
COPY --from=builder /app/target/classes/application-*.yml ./
COPY --from=builder /app/config ./config

# Expose port
EXPOSE 8083

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8083/actuator/health || exit 1

# Start the application
CMD ["java", "-jar", "app.jar"]