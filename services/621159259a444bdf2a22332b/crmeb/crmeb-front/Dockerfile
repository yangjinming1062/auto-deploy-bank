# Multi-stage build for CRMEB Java application
# Stage 1: Build the application with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy parent POM and all modules
COPY pom.xml .
COPY crmeb-service ./crmeb-service
COPY crmeb-common ./crmeb-common
COPY crmeb-admin ./crmeb-admin
COPY crmeb-front ./crmeb-front

# Build the entire project (parent + all modules)
RUN mvn clean package -DskipTests -B

# Stage 2: Create runtime image
FROM eclipse-temurin-17-jre-alpine

WORKDIR /app

# Create target directory for JAR mounting
RUN mkdir -p /app/target

# Copy the built JAR from builder stage
COPY --from=builder /app/crmeb-front/target/Crmeb-front.jar /app/target.jar

# Expose the internal port (8081)
EXPOSE 8081

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8081/ || exit 1

# Start the application
CMD ["java", "-jar", "/app/target.jar"]