# Stage 1: Build
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY login-registration-springboot-hibernate-jsp-auth/pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY login-registration-springboot-hibernate-jsp-auth/src ./src

# Build the application with repackaging to create executable WAR (skip tests for docker build)
RUN mvn clean package -DskipTests -B spring-boot:repackage

# Stage 2: Runtime
FROM eclipse-temurin:8-jre-alpine

# Install curl for healthcheck
RUN apk add curl --no-cache

WORKDIR /app

# Copy the built executable WAR from builder stage to app directory
COPY --from=builder /app/target/*.war /app/app.war

# Expose the application port
EXPOSE 8080

# Copy WAR to mounted volume for security scanning and run app
CMD ["sh", "-c", "cp /app/app.war /app/target.jar && java -jar /app/app.war"]