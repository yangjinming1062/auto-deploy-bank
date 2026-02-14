# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml and source files
COPY pom.xml .
COPY src ./src

# Build the package with dependencies (create uber jar)
RUN mvn clean package -Dmaven.test.skip=true -B && \
    mv target/fastjson-1.2.84-SNAPSHOT-jar-with-dependencies.jar target.jar

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1000 app && \
    adduser -u 1000 -G app -s /bin/sh -D app

# Copy the JAR file from builder stage
COPY --from=builder /app/target.jar app.jar

# Change ownership to non-root user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose the application port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]