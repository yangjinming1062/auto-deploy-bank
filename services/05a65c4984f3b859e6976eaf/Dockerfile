# Stage 1: Build the uber-jar application
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build uber-jar (single JAR with all dependencies)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install curl for healthcheck
RUN apk add --no-cache curl

# Create non-root user for security
RUN addgroup -S quarkus && adduser -S quarkus -G quarkus
USER quarkus

# Copy the uber-jar from builder stage
# Quarkus uber-jar naming: quarkus-app-{version}-runner.jar
COPY --from=builder /app/target/quarkus-app-1.0.0-SNAPSHOT-runner.jar target.jar

# Expose the HTTP port
EXPOSE 8080

# Set environment variables
ENV QUARKUS_HTTP_PORT=8080
ENV QUARKUS_HTTP_HOST=0.0.0.0

# Run the application
CMD ["java", "-jar", "target.jar"]