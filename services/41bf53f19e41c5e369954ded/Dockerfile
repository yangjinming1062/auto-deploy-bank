# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy pom.xml first for dependency caching
COPY bootdo/pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY bootdo/src ./src

# Build the JAR (skip tests for container build)
RUN mvn clean package -DskipTests -B -q

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN addgroup --system app && adduser --system --ingroup app --no-create-home --shell /bin/false app

# Copy the built JAR from builder stage and rename to target.jar for security scanning
# Also save to /output for host access
COPY --from=builder /app/target/*.jar target.jar
RUN mkdir -p /output && cp target.jar /output/target.jar

# Change ownership to non-root user
RUN chown -R app:app /app /output
RUN chmod 644 /output/target.jar

# Switch to non-root user
USER app

# Expose the application port (default Spring Boot port)
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

# Run the application with Java 17 compatibility flags for Spring Boot 2.0.x
ENTRYPOINT ["java", \
  "--add-opens=java.base/java.lang=ALL-UNNAMED", \
  "--add-opens=java.base/java.lang.reflect=ALL-UNNAMED", \
  "--add-opens=java.base/java.util=ALL-UNNAMED", \
  "-jar", "target.jar"]