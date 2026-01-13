# Stage 1: Build with Maven (Java 8 for compatibility)
FROM maven:3.9-eclipse-temurin-8 AS builder

WORKDIR /app

# Copy the entire project for multi-module build
COPY . .

# Create a fake .git directory to satisfy git-commit-id-plugin
RUN git init && \
    git config user.email "build@example.com" && \
    git config user.name "Build System" && \
    git add . && \
    git commit -m "Initial commit" 2>/dev/null || true

# Build the entire project (skip tests)
RUN mvn clean install -Dmaven.test.skip=true -B

# Stage 2: Runtime image (Java 17 for security and performance)
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create logs directory
RUN mkdir -p logs

# Copy the moss-web fat JAR from builder stage
# Note: moss-web.jar is the Spring Boot executable JAR (~76MB)
# moss-web-sources.jar is only ~1.7MB with source files only
COPY --from=builder /app/moss-web/target/moss-web.jar target.jar

# Expose the application port
EXPOSE 8086

# Run the application with JVM args to open Java modules for XStream/Eureka
# These are needed because the application was built for Java 8 but runs on Java 17
CMD ["java", \
    "--add-opens=java.base/java.util=ALL-UNNAMED", \
    "--add-opens=java.base/java.lang=ALL-UNNAMED", \
    "--add-opens=java.base/java.lang.reflect=ALL-UNNAMED", \
    "--add-opens=java.base/java.text=ALL-UNNAMED", \
    "--add-opens=java.desktop/java.awt.font=ALL-UNNAMED", \
    "-jar", "target.jar"]