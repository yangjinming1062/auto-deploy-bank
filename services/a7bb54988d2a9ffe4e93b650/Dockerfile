# Stage 1: Builder using Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy entire project structure first (required for multi-module Maven build)
COPY . .

# Build the application (skip tests for production build)
# Build console modules which have Spring Boot executable JAR with mainClass
# Add JVM args to fix Lombok compatibility with Java 17
RUN export MAVEN_OPTS="--add-opens=jdk.compiler/com.sun.tools.javac.code=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.comp=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.main=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.model=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.parser=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.processing=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED --add-opens=jdk.compiler/com.sun.tools.javac.jvm=ALL-UNNAMED" && \
    mvn clean package -DskipTests -B -pl :sparta-uofs-console,:sparta-ucdn-console -am

# Stage 2: Runtime image
FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app

# Create non-root user for security
RUN addgroup -S app && adduser -S app -G app

# Copy the built executable JAR from builder stage
# These are the console modules with spring-boot-maven-plugin configured
# Named as target.jar for security scanning volume mount
COPY --from=builder /app/Sparta/sparta-uofs-console/target/sparta-uofs-console-*.jar target.jar
COPY --from=builder /app/Sparta/sparta-ucdn-console/target/sparta-ucdn-console-*.jar app-ucdn.jar

# Copy configuration files required by the application
COPY --from=builder /app/system ./system
COPY --from=builder /app/config/application.yaml ./config/application.yaml

# Create data directories for file system and volumes
RUN mkdir -p /app/data/files /app/data/volumes && chown -R app:app /app

# Change ownership to non-root user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose the application port
EXPOSE 7580

# Health check (check if the app is responding on port 7580)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:7580/ || exit 1

# Run the application (sparta-uofs-console is the main service)
CMD ["java", "-jar", "target.jar"]