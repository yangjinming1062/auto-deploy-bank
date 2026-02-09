# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-21 AS builder

WORKDIR /app

# Copy root pom.xml (parent POM)
COPY pom.xml .
COPY server/pom.xml ./server/pom.xml

# Create server source directory structure
COPY server/src ./server/src

# Install parent POM first, then build server module (skip tests for image creation)
RUN mvn install -N -B && \
    cd server && \
    mvn clean package -DskipTests -B

# Stage 2: Runtime stage
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/server/target/server.jar target.jar

# Expose the application port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "target.jar"]