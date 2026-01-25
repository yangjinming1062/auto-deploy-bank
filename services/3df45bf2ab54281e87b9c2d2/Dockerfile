# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy entire project including all module pom.xml files and source code
COPY . .

# Build the project
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create necessary directories
RUN mkdir -p logs temp

# Copy the built jar from builder stage to target.jar (for volume mount)
COPY --from=builder /app/ruoyi-admin/target/ruoyi-admin.jar target.jar

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ || exit 1

# Run the application
ENTRYPOINT ["java", "-jar", "target.jar"]