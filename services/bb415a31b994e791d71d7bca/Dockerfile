# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY myapp/pom.xml ./myapp/

# Download dependencies
RUN cd /app/myapp && mvn dependency:go-offline -B

# Copy source code
COPY myapp/src ./myapp/src

# Build the project (Spring Boot repackaged JAR)
RUN cd /app/myapp && mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the Spring Boot repackaged JAR (includes all dependencies)
COPY --from=builder /app/myapp/target/mycamel-app-1.0.0-SNAPSHOT.jar /app/app.jar
COPY --from=builder /app/myapp/target/mycamel-app-1.0.0-SNAPSHOT.jar /app/target.jar

# Copy application.properties
COPY --from=builder /app/myapp/src/main/resources/application.properties /app/

# Use proper shell for entrypoint
SHELL ["/bin/sh", "-c"]

# Set environment variables
ENV JAVA_OPTS="-Xms256m -Xmx512m"

# Healthcheck - check if the Java process is running and port is listening
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/hello || exit 1

# Run the Spring Boot application
ENTRYPOINT ["java", "-jar", "app.jar"]