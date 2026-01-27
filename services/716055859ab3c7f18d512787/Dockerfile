# Stage 1: Build
FROM eclipse-temurin:17-jdk-alpine AS builder

WORKDIR /app

# Copy project files
COPY gradle ./gradle
COPY gradlew ./
COPY gradlew.bat ./
COPY settings.gradle.kts ./
COPY build.gradle.kts ./
COPY gradle.properties ./
COPY samples ./samples
COPY core ./core
COPY shipshape ./shipshape
COPY kaliningraph ./kaliningraph

# Make gradlew executable
RUN chmod +x gradlew

# Remove all sample files except HelloKotlingrad.kt
RUN ls samples/src/main/kotlin/ai/hypergraph/kotlingrad/samples/*.kt | grep -v HelloKotlingrad.kt | xargs rm -f 2>/dev/null || true

# Build the distribution (includes all dependencies)
RUN ./gradlew :samples:installDist --no-daemon -x test && \
    ls samples/build/libs/ && \
    cp samples/build/libs/samples-*.jar samples/build/libs/target.jar

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copy the distribution from builder
COPY --from=builder /app/samples/build/install/samples samples

# Copy built jar at runtime (after volume mount) for security scanning
COPY --from=builder /app/samples/build/libs/target.jar /app/target.jar.copy

# Run the application - copies jar to mounted volume location
CMD ["sh", "-c", "cp /app/target.jar.copy /app/target.jar && samples/bin/samples"]