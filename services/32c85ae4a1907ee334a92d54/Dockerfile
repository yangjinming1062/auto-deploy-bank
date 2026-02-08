# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy entire project first
COPY . .

# Build the project with thin layout disabled to create proper fat jar
RUN mvn clean package -DskipTests -B -pl spring-cloud-function-web -am \
    -Dspring-boot.repackage.use-thin-layout=false \
    -Dorg.springframework.boot.experimental.spring-boot-thin.skip=true

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install su-exec and netcat for healthcheck
RUN apk add --no-cache su-exec netcat-openbsd

# Create non-root user for security
RUN addgroup -S spring && adduser -S spring -G spring

# Copy the JAR file as target.jar for security scanning
COPY --from=builder /app/spring-cloud-function-web/target/spring-cloud-function-web-5.0.2-SNAPSHOT.jar /app/target.jar

# Set ownership for non-root user
RUN chown -R spring:spring /app

# Run as non-root user
USER spring

# Expose default Spring Boot port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "target.jar"]