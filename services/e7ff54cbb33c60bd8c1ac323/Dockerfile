# Stage 1: Build with Maven (Java 17)
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Set MAVEN_OPTS for Spring Boot 2.0.4 compatibility with Java 17
ENV MAVEN_OPTS="--add-opens=jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED \
  --add-opens=jdk.compiler/com.sun.tools.javac.attr=ALL-UNNAMED \
  --add-opens=jdk.compiler/com.sun.tools.javac.code=ALL-UNNAMED \
  --add-opens=jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED \
  --add-opens=jdk.compiler/com.sun.tools.javac.jvm=ALL-UNNAMED \
  --add-opens=jdk.compiler/com.sun.tools.javac.main=ALL-UNNAMED \
  --add-opens=jdk.compiler/com.sun.tools.javac.model=ALL-UNNAMED \
  --add-opens=jdk.compiler/com.sun.tools.javac.parser=ALL-UNNAMED \
  --add-opens=jdk.compiler/com.sun.tools.javac.processing=ALL-UNNAMED \
  --add-opens=jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED \
  --add-opens=jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED \
  --add-opens=java.base/java.lang=ALL-UNNAMED \
  --add-opens=java.base/java.lang.invoke=ALL-UNNAMED \
  --add-opens=java.base/java.lang.reflect=ALL-UNNAMED \
  --add-opens=java.base/java.io=ALL-UNNAMED \
  --add-opens=java.base/java.util=ALL-UNNAMED \
  --add-opens=java.base/java.util.concurrent=ALL-UNNAMED \
  --add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED \
  --add-opens=java.base/jdk.internal.reflect=ALL-UNNAMED \
  --add-opens=java.base/sun.nio.ch=ALL-UNNAMED \
  --add-opens=java.base/sun.security.action=ALL-UNNAMED"

# Copy the entire project structure (parent pom and all modules)
COPY . .
# Build the web module and its dependencies
RUN mvn clean package -DskipTests -B -pl easyreport-web -am

# Stage 2: Runtime image (Java 17)
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install curl for health checks
RUN apk add --no-cache curl

# Create a non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Copy the JAR file from builder stage
COPY --from=builder /app/easyreport-web/target/easyreport-web.jar target.jar

# Change ownership to appuser
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Health check - using root path since actuator is not enabled
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/ || exit 1

# Expose port
EXPOSE 8080

# Run the application with Java 17 compatibility flags for Spring Boot 2.0.x
CMD ["java", \
     "--add-opens=java.base/java.lang=ALL-UNNAMED", \
     "--add-opens=java.base/java.lang.invoke=ALL-UNNAMED", \
     "--add-opens=java.base/java.lang.reflect=ALL-UNNAMED", \
     "--add-opens=java.base/java.io=ALL-UNNAMED", \
     "--add-opens=java.base/java.util=ALL-UNNAMED", \
     "--add-opens=java.base/java.util.concurrent=ALL-UNNAMED", \
     "--add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED", \
     "--add-opens=java.base/jdk.internal.reflect=ALL-UNNAMED", \
     "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED", \
     "--add-opens=java.base/sun.security.action=ALL-UNNAMED", \
     "-jar", "target.jar"]