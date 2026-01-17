# Stage 1: Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory to the project root
WORKDIR /app/eladmin

# Copy pom.xml first for dependency caching
COPY pom.xml ./
# Download dependencies (including parent pom modules)
RUN mvn dependency:go-offline -B || true

# Copy entire project source code
COPY . .

# Build the application (skip tests, build eladmin-system and dependencies)
RUN mvn clean package -DskipTests -B -pl eladmin-system -am

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create non-root user for security
RUN addgroup -S app && adduser -S -G app app

# Copy the built JAR from builder stage
# The JAR is built in eladmin-system/target/ with name eladmin-system-1.1.jar
COPY --from=builder /app/eladmin/eladmin-system/target/eladmin-system-1.1.jar app.jar
COPY --from=builder /app/eladmin/eladmin-system/target/eladmin-system-1.1.jar target.jar

# Copy the JAR to /exports for host access (security scanning)
COPY --from=builder /app/eladmin/eladmin-system/target/eladmin-system-1.1.jar /exports/target.jar

# Change ownership to non-root user
RUN chown -R app:app /app && chown app:app /exports

# Switch to non-root user
USER app

# Expose the application port
EXPOSE 8000

# Health check - check if port is listening
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/ || exit 1

# Run the application
CMD ["java", "-jar", "app.jar"]