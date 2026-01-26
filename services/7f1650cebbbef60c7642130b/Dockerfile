# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy the Core module structure first
COPY neuroph-2.9/pom.xml neuroph-2.9/pom.xml
COPY neuroph-2.9/Core/pom.xml neuroph-2.9/Core/pom.xml
COPY neuroph-2.9/Core/src neuroph-2.9/Core/src

# Build only the Core module (skip tests)
RUN cd neuroph-2.9/Core && mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app

# Copy the JAR file from builder
COPY --from=builder /app/neuroph-2.9/Core/target/neuroph-core-2.94.jar app.jar

# Expose the port (8080 is hardcoded in NeurophService)
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]