# Stage 1: Build
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Copy pom.xml first for dependency caching
COPY pom.xml ./
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the project (skip tests for container build)
RUN mvn clean package -DskipTests -B -pl . -am

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /opt/app

# Copy the built JAR from builder stage
COPY --from=builder /build/target/*.jar app.jar

# Expose port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]