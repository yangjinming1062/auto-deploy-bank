# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application (skip tests)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install wget for healthcheck
RUN apk add --no-cache wget

# Create non-root user for security
RUN addgroup -S app && adduser -S -G app app

# Copy the built JAR from builder stage
COPY --from=builder /app/target/*.jar app.jar

# Change ownership to non-root user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose the application port
EXPOSE 8081

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8081/ || exit 1

# Run the application
CMD ["java", "-jar", "app.jar"]