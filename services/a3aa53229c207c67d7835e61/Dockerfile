# Multi-stage build for Micrometer Javalin Sample Application

# Stage 1: Build stage using Maven with Eclipse Temurin 17
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy Maven project files
COPY samples/micrometer-samples-javalin/pom.xml .

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code
COPY samples/micrometer-samples-javalin/src src

# Build the application with shaded JAR
RUN mvn clean package shade:shade -DskipTests -B

# Stage 2: Runtime stage using Eclipse Temurin 17 JRE
FROM eclipse-temurin:17-jdk-alpine

# Install curl for healthcheck
RUN apk add --no-cache curl

# Set working directory
WORKDIR /app

# Copy the shaded JAR from builder stage (it should be the original JAR name with -shaded suffix)
COPY --from=builder /app/target/micrometer-samples-javalin-*.jar app.jar

# Create a symlink for security scanning
RUN ln -s app.jar target.jar

# Expose port 8080
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/ || exit 1

# Run the application
CMD ["java", "-jar", "app.jar"]