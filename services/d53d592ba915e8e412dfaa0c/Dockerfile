# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy entire project
COPY . .

# Build the application (repackage is now part of package phase)
RUN mvn clean package -DskipTests -B -pl spring-shell-samples/spring-shell-sample-spring-boot -am

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create directory for security scanning
RUN mkdir -p /data

# Copy the built JAR file (original.jar is source, target.jar is mounted)
COPY --from=builder /app/spring-shell-samples/spring-shell-sample-spring-boot/target/*.jar /data/original.jar

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the port (configured in application.properties)
EXPOSE 40351

# Run the application via entrypoint script
ENTRYPOINT ["/entrypoint.sh"]