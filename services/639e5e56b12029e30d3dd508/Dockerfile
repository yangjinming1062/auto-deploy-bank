# Stage 1: Build
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source and build
COPY src ./src
RUN mvn clean package -DskipTests -Dlicense.skip=true -B

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage to target.jar for volume mount and security scanning
COPY --from=builder /app/target/capsule-*.jar /app/target.jar

# Expose the HTTP server port
EXPOSE 8080

# Run the HTTP server main class
CMD ["java", "-cp", "/app/target.jar", "io.usethesource.capsule.CapsuleHttpServer"]