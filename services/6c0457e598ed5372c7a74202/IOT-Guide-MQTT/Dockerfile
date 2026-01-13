# Multi-stage build for IOT-Guide-MQTT
# Stage 1: Builder with Maven and JDK 8 (project uses Java 8)
FROM maven:3.6-openjdk-8 AS builder

# Set working directory
WORKDIR /workspace

# Copy entire project structure (parent at root, modules as subdirectories)
COPY . .

# Install parent POM first
RUN mvn install -DskipTests -B -N

# Build TSL dependency and install it
RUN mvn clean install -DskipTests -B -pl IOT-Guide-TSL

# Build MQTT module (uses TSL from repository)
RUN mvn clean install spring-boot:repackage -DskipTests -B -pl IOT-Guide-MQTT

# Stage 2: Runtime image with JRE 8
FROM eclipse-temurin:8-jre

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /workspace/IOT-Guide-MQTT/target/IOT-Guide-MQTT-*.jar app.jar

# Expose the MQTT port
EXPOSE 9876

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q -O- http://localhost:9876/actuator/health || exit 1

# Run the application (use -jar for Spring Boot executable JAR)
CMD ["java", "-jar", "app.jar"]