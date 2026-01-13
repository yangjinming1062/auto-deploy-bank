# Multi-stage build for Gradle project

# Stage 1: Build the project
FROM gradle:7.6-jdk11 AS builder

WORKDIR /app

# Copy Gradle files
COPY build.gradle .
COPY settings.gradle .
COPY gradle.properties .
COPY gradlew .
COPY gradlew.bat .
COPY gradle/ gradle/
COPY .gradle/ .gradle/

# Copy the crawler4j module
COPY crawler4j/ ./crawler4j/

# Copy the examples base module (contains BasicCrawler)
COPY crawler4j-examples/crawler4j-examples-base/ ./crawler4j-examples/crawler4j-examples-base/

# Copy the web service module
COPY crawler4j-examples/crawler4j-examples-web/ ./crawler4j-examples/crawler4j-examples-web/

# Build the project
RUN ./gradlew :crawler4j-examples-web:shadowJar --no-daemon

# Stage 2: Runtime image
FROM eclipse-temurin:11-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/crawler4j-examples/crawler4j-examples-web/build/libs/crawler4j-web-1.0.0.jar app.jar

# Create a copy of the JAR for security scanning
RUN cp app.jar target.jar

# Expose the port
EXPOSE 40326

# Run the application
CMD ["java", "-jar", "app.jar"]