# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code (all modules are now at root of build context)
COPY . .
RUN mvn clean package -DskipTests -B -pl eladmin-system -am

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

# Install wget for healthcheck
RUN apk add --no-cache wget

WORKDIR /app

# Create non-root user for security
RUN addgroup -S app && adduser -S app -G app

# Copy the built JAR from builder stage and rename for security scanning
COPY --from=builder /app/eladmin-system/target/*.jar target.jar

# Change ownership to non-root user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose the application port
EXPOSE 8000

# Health check - test root endpoint (Spring Security may return 401 or 403, which is fine)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/ 2>/dev/null || exit 1

# Run the application
CMD ["java", "-jar", "target.jar"]