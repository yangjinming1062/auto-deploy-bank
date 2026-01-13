# Multi-stage Docker build for WxJava Demo Application
# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /build

# Copy pom.xml and src
COPY demo-app/pom.xml ./demo-app/
COPY demo-app/src ./demo-app/src

# Build the application
WORKDIR /build/demo-app
RUN mvn clean package -DskipTests -B

# Stage 2: Create runtime image
FROM maven:3.9-eclipse-temurin-17

# Set working directory
WORKDIR /app

# Copy the built JAR from the builder stage
COPY --from=builder /build/demo-app/target/wx-java-demo-*.jar app.jar

# Also copy it to a location for volume mounting (not conflicting with VOLUME)
RUN mkdir -p /data && cp app.jar /data/target.jar

# Create a volume for security scanning
VOLUME ["/data"]

# Expose port 40358
EXPOSE 40358

# Health check (using curl)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:40358/api/demo/health || exit 1

# Run the application
CMD ["java", "-jar", "app.jar"]