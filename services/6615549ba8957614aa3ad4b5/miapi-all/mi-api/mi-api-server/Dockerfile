# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application (skip tests, use staging profile)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:8-jre-alpine

# Create non-root user for security
RUN addgroup -S app && adduser -S app -G app

WORKDIR /home/home/ubuntu/deploy-projects

# Create log directory
RUN mkdir -p /home/home/ubuntu/deploy-projects/log/mi-api && chown -R app:app /home/home/ubuntu/deploy-projects

# Copy the built JAR file from builder stage
COPY --from=builder /app/target/mi-api-server-1.0.0-SNAPSHOT.jar app.jar

# Switch to non-root user
USER app

# Expose the application port
EXPOSE 8999

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8999/actuator/health || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "-Xms512M", "-Xmx512M", "-XX:+UseG1GC", "app.jar"]