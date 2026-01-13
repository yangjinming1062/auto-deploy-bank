# Root Dockerfile for multi-service deployment
# This file serves as an entry point for the complete yuzi-generator platform

# Stage 1: Build backend
FROM maven:3.9-eclipse-temurin-17 AS backend-builder

WORKDIR /build

# Build yuzi-generator-maker first
COPY yuzi-generator-maker/pom.xml .
COPY yuzi-generator-maker/src ./src
RUN mvn clean install -DskipTests

# Build backend
COPY yuzi-generator-web-backend/pom.xml .
COPY yuzi-generator-web-backend/src ./src
RUN mvn clean package -DskipTests

# Stage 2: Backend runtime
FROM eclipse-temurin:17-jdk

WORKDIR /app

COPY --from=backend-builder /build/target/*.jar target.jar

EXPOSE 8120

CMD ["java", "-jar", "target.jar", "--spring.profiles.active=prod"]