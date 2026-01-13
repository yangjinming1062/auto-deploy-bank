# Multi-stage build for Discord4J Bot
# Stage 1: Build the application
FROM eclipse-temurin:17-jdk AS builder

WORKDIR /app

# Copy Gradle wrapper and build files
COPY gradlew .
COPY gradle/ ./gradle/
COPY build.gradle .
COPY settings.gradle .
COPY gradle.properties .
COPY .git/ ./.git/
COPY core/ ./core/
COPY rest/ ./rest/
COPY gateway/ ./gateway/
COPY common/ ./common/
COPY voice/ ./voice/
COPY oauth2/ ./oauth2/
COPY app/ ./app/

# Make gradlew executable
RUN chmod +x gradlew

# Download dependencies and build the application
RUN ./gradlew :app:build -x test

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy built application from builder stage
COPY --from=builder /app/app/build/libs/discord4j-app-1.0.0-all.jar app.jar

# Expose the HTTP port
EXPOSE 40158

# Set environment variables
ENV JAVA_OPTS="-Xmx512m -Xms256m"

# Run the application
CMD ["java", "-jar", "app.jar"]