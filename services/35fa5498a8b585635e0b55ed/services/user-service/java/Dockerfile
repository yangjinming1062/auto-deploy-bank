# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml first for dependency caching
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source files
COPY src ./src

# Build the application (skip tests for faster build)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre

WORKDIR /app

# Create non-root user for security
RUN groupadd --system miyagiuser && useradd --system --gid miyagiuser --shell /bin/false --create-home miyagiuser

# Copy the built JAR from builder stage
COPY --from=builder /app/target/*.jar app.jar

# Copy Application Insights agent if exists
RUN if [ -f /app/target/agent/applicationinsights-agent.jar ]; then cp /app/target/agent/applicationinsights-agent.jar /app/applicationinsights-agent.jar; fi

# Copy Application Insights config if exists
RUN if [ -f /app/target/classes/applicationinsights.json ]; then cp /app/target/classes/applicationinsights.json /app/applicationinsights.json; fi

# Change ownership to non-root user
RUN chown -R miyagiuser:miyagiuser /app

USER miyagiuser

# Expose the application port
ARG PORT=8901
EXPOSE ${PORT}

# Run the application
CMD ["java", "-jar", "app.jar"]