# Multi-stage build for Hello Java Security application
# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy pom.xml first for better layer caching
COPY pom.xml .

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:8-jre

WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/target/javasec-1.15.jar target.jar

# Create volume for temporary files and security scanning
VOLUME /tmp
VOLUME /app

# Expose the application port
EXPOSE 8888

# Set the entrypoint
ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", "-jar", "target.jar"]

# Use docker profile
CMD ["--spring.profiles.active=docker"]