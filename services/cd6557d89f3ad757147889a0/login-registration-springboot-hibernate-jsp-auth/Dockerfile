# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source and build
COPY src ./src
RUN mvn clean package -DskipTests -B && mv target/*.war target/app.war

# Stage 2: Runtime
FROM eclipse-temurin:8-jre-alpine

WORKDIR /app

# Install curl for healthcheck
RUN apk add curl --no-cache

# Copy the WAR file from builder
COPY --from=builder /app/target/*.war app.war

# Expose port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.war"]