# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy source code and pom.xml
COPY pom.xml .
COPY src ./src

# Build the project with shade plugin to create executable JAR
# Skip test compilation and execution to avoid Java module issues
RUN mvn clean package -Dmaven.test.skip=true -B

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine AS runtime

WORKDIR /app

# Copy the shaded JAR from builder stage
# The shade plugin outputs to target.jar in project root
COPY --from=builder /app/target.jar app.jar

# Create a non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app
USER appuser

# Expose the application port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/api/ || exit 1

# Run the application
CMD ["java", "-jar", "app.jar"]