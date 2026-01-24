# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime stage
FROM amazoncorretto:8-alpine-jdk

WORKDIR /app

# Copy the built JAR from builder stage (named as target.jar for volume mount)
COPY --from=builder /app/target/*.jar target.jar

# Run the application
CMD ["java", "-jar", "target.jar"]