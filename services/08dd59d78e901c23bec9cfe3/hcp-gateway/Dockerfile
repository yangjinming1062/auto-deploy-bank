# ===================================================================
# Multi-stage build for HCP Gateway
# ===================================================================

# Stage 1: Build stage with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy pom.xml and download dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application
RUN mvn clean package -DskipTests -B

# ===================================================================

# Stage 2: Runtime stage
FROM eclipse-temurin-17-jre-alpine

# Set working directory
WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/target/hcp-gateway.jar app.jar

# Expose port
EXPOSE 38080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:38080/actuator/health || exit 1

# Run the application
CMD ["java", "-jar", "app.jar"]