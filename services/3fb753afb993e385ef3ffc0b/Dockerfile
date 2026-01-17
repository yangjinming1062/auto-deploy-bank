# Stage 1: Builder
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy all source files first for multi-module Maven project
COPY . .

# Remove config file to use command-line parameters only
RUN rm -f em.yaml

# Build the JAR (skip tests as per requirements)
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Create non-root user for security
RUN addgroup -S evomaster && adduser -S evomaster -G evomaster

# Copy the built JAR from builder stage to both app.jar and target.jar
COPY --from=builder /app/core/target/evomaster.jar app.jar
COPY --from=builder /app/core/target/evomaster.jar target.jar

# Change ownership to non-root user
RUN chown -R evomaster:evomaster /app

# Switch to non-root user
USER evomaster

# Expose SUT controller port
EXPOSE 40100

# Run EvoMaster with JVM options for JDK 17 module access
# Use black-box mode to avoid needing external SUT driver connection
# For black-box REST API testing, specify --bbSwaggerUrl with OpenAPI schema URL
# Set maxTime to 24h for continuous running (or adjust as needed)
CMD ["java", \
     "-Xmx4G", \
     "--add-opens=java.base/java.net=ALL-UNNAMED", \
     "--add-opens=java.base/java.util=ALL-UNNAMED", \
     "-jar", "app.jar", \
     "--runningInDocker", "true", \
     "--blackBox", "true", \
     "--bbSwaggerUrl", "https://petstore.swagger.io/v2/swagger.json", \
     "--maxTime", "24h"]