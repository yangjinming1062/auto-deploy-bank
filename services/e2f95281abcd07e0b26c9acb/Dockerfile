# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy parent pom.xml first for dependency caching
COPY pom.xml .
COPY dhorse-api/pom.xml dhorse-api/
COPY dhorse-application/pom.xml dhorse-application/
COPY dhorse-infrastructure/pom.xml dhorse-infrastructure/
COPY dhorse-agent/pom.xml dhorse-agent/
COPY dhorse-rest/pom.xml dhorse-rest/

# Download dependencies
RUN mvn dependency:go-offline -B

# Copy source code for all modules (dependencies need to be compiled too)
COPY dhorse-api/src dhorse-api/src
COPY dhorse-infrastructure/src dhorse-infrastructure/src
COPY dhorse-application/src dhorse-application/src
COPY dhorse-agent/src dhorse-agent/src
COPY dhorse-rest/src dhorse-rest/src

# Build all modules and install to local repo (skip tests)
RUN mvn clean install -DskipTests -B -Dmaven.test.skip=true && \
    # Copy dependencies to lib folder for classpath execution
    mvn dependency:copy-dependencies -B -f dhorse-rest/pom.xml -DoutputDirectory=lib

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create directories for data and logs
RUN mkdir -p /app/data/db /app/data/logs /app/data/temp /app/data/storage /app/conf /app/static /app/lib

# Copy the built JAR file as target.jar for security scanning
COPY --from=builder /app/dhorse-rest/target/dhorse-rest-*.jar app.jar

# Copy dependencies
COPY --from=builder /app/dhorse-rest/lib /app/lib

# Copy configuration file
COPY conf/dhorse.yml /app/conf/dhorse.yml

# Copy static files (frontend UI)
COPY static/ /app/static/

# Expose the application port
EXPOSE 8100

# Set environment variables
ENV DATA_PATH=/app/data
ENV LOG_PATH=/app/data/logs
ENV SPRING_CONFIG_LOCATION=/app/conf/
ENV CLASSPATH=/app/app.jar:/app/lib/*

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8100/ || exit 1

# Run the application with classpath
CMD ["java", "-Djava.security.egd=file:/dev/./urandom", "-cp", "/app/app.jar:/app/lib/*", "org.dhorse.rest.DHorseBootstrap", "--spring.config.location=/app/conf/dhorse.yml"]