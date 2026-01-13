# Multi-stage build for Java application
# Stage 1: Build with Maven (Java 8)
FROM maven:3.9-eclipse-temurin-8 AS builder

# Set working directory
WORKDIR /app

# Copy pom.xml first for better caching
COPY pom.xml .

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application (skip assembly plugin)
RUN mvn clean package -DskipTests -B -Dfast-build=true

# Stage 2: Runtime image (Java 8)
FROM eclipse-temurin:8-jre-alpine

WORKDIR /app

# Copy WAR from builder stage (Spring Boot creates executable WAR)
# The spring-boot:repackage creates lavagna-jetty-console.war
COPY --from=builder /app/target/lavagna-jetty-console.war /app/app.war

# Create a copy for the volume mount location
RUN cp /app/app.war /app/app.jar

# Expose port 8080
EXPOSE 8080

# Use an entrypoint script to handle the volume mount copy
COPY <<EOF /entrypoint.sh
#!/bin/sh
# Ensure target.jar exists and has the correct content
if [ -d "/app/target.jar" ]; then
  # If it's a directory, remove it and create a file
  rm -rf /app/target.jar
fi
# Copy JAR to target location
cp /app/app.jar /app/target.jar
# Run the application
exec java -jar /app/app.jar
EOF

RUN chmod +x /entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]