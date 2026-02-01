# Stage 1: Builder
FROM eclipse-temurin:21-jdk AS builder

WORKDIR /app

# Copy Gradle wrapper and build files
COPY gradlew ./
COPY gradle ./gradle
COPY build.gradle.kts ./
COPY settings.gradle.kts ./
COPY book/build.gradle.kts ./book/
COPY book/src ./book/src
COPY book/src/lib ./book/src/lib
COPY src ./src

# Make gradlew executable
RUN chmod +x gradlew

# Build the project (creates fat JAR with all dependencies)
RUN ./gradlew jar -x test --no-daemon

# Stage 2: Runtime
FROM eclipse-temurin:21-jre

WORKDIR /app

# Create non-root user for security
RUN groupadd --system app && useradd --system --gid app --shell /bin/false --home-dir /app app

# Copy the built JAR file from builder stage
COPY --from=builder /app/build/libs/solon-read-1.0-SNAPSHOT.jar target.jar

# Copy configuration files
COPY conf/conf.yml ./
COPY conf ./conf
COPY src/main/resources/app.yml ./

# Create data directory for SQLite database
RUN mkdir -p /app/data && chown -R app:app /app

# Switch to non-root user
USER app

# Expose the application port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ || exit 1

# Run the application with JVM arguments to fix Gson reflection issues with Java 21
CMD ["java", "--add-opens=java.base/java.time=ALL-UNNAMED", "-jar", "target.jar"]