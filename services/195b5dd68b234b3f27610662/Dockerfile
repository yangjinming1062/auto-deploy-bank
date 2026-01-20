# Stage 1: Build with Maven
FROM maven:3.8.6-openjdk-8 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .

# Copy local JAR dependencies first (needed for system-scoped dependencies)
COPY resources/library/ ./resources/library/

# Copy webapp content to static resources so Spring Boot serves it as executable JAR
# Spring Boot only serves static content from classpath:/static, /public, /resources when running as JAR
COPY src/main/webapp ./src/main/resources/static/

# Download dependencies (go-offline)
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application (skip tests for faster build)
# Use the CelloSpringBoot profile to create executable jar with dependencies
RUN mvn clean package -P CelloSpringBoot -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:8-jre-alpine

WORKDIR /app

# Create directories for Derby database and results
RUN mkdir -p resources/derbydb2 cello_results

# Copy the built JAR to a fixed location (not affected by volume mount)
COPY --from=builder /app/target/*.jar /app/built-app.jar

# Copy local JAR dependencies to classpath
COPY --from=builder /app/resources/library/ /app/resources/library/

# Set environment variables
ENV SPRING_DATASOURCE_URL="jdbc:derby:resources/derbydb2;create=true"
ENV SPRING_DATASOURCE_DRIVER_CLASS_NAME="org.apache.derby.jdbc.EmbeddedDriver"
ENV SERVER_PORT="8080"
ENV CELLO_USER_DB_NAME="CELLO"
ENV CELLO_RESULT_PATH="/app/cello_results"
ENV CELLO_SRC_PATH="/app"

# Expose the application port
EXPOSE 8080

# Health check - check if Tomcat is listening on port 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD nc -z localhost 8080 || exit 1

# Run the application
# Copy built JAR to target.jar (for security scanning), then run
# Remove existing Derby database directory if it exists to allow fresh initialization
CMD cp /app/built-app.jar /app/target.jar && rm -rf /app/resources/derbydb2 && java -jar /app/target.jar