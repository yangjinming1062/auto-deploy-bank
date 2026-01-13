# Multi-stage build for Spring Boot application
# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy entire project for proper Maven reactor support
COPY . .

# Build only the eladmin-system module
RUN mvn clean package -pl eladmin-system -am -DskipTests -B

# Stage 2: Runtime image
FROM maven:3.9-eclipse-temurin-17

WORKDIR /app

# Copy JAR from builder stage (from eladmin-system module)
COPY --from=builder /app/eladmin-system/target/*.jar target.jar

# Create /scans directory for volume mount (security scanning)
RUN mkdir -p /scans

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD wget -q -O- http://localhost:8000/actuator/health || exit 1

# Run the application
CMD ["java", "-jar", "target.jar"]