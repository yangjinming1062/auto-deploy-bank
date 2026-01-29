# Stage 1: Build with Gradle
FROM eclipse-temurin:17-jdk-alpine AS builder

WORKDIR /app

# Copy Gradle wrapper and build files
COPY gradlew .
COPY gradle ./gradle
COPY build.gradle .
COPY settings.gradle .
COPY desktop/build.gradle ./desktop/build.gradle
COPY core/build.gradle ./core/build.gradle
COPY sdk/build.gradle ./sdk/build.gradle
COPY littleproxy/build.gradle ./littleproxy/build.gradle
COPY sample-plugin/build.gradle ./sample-plugin/build.gradle

# Copy libs directories (local JAR dependencies)
COPY desktop/libs ./desktop/libs
COPY sdk/libs ./sdk/libs

# Copy source directories
COPY core/src ./core/src
COPY desktop/src ./desktop/src
COPY sdk/src ./sdk/src
COPY littleproxy/src ./littleproxy/src
COPY sample-plugin/src ./sample-plugin/src

# Make gradlew executable and build all subprojects first, then the desktop fatJar
RUN chmod +x gradlew && \
    ./gradlew assemble --no-daemon && \
    ./gradlew :desktop:fatJar -x test --no-daemon

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/desktop/build/libs/desktop-*-all.jar target.jar

# Copy config.ini for runtime configuration
COPY config.ini .

# Expose the proxy port
EXPOSE 8085

# Run the application
CMD ["java", "-jar", "target.jar"]