# ===================================================================
# Multi-stage build for HCP Gateway
# ===================================================================

# Stage 1: Build stage with Maven (Java 17)
FROM maven:3.9-eclipse-temurin-17 AS builder

# Set working directory
WORKDIR /app

# Copy all module directories (required for Maven to resolve dependencies)
COPY pom.xml .
COPY hcp-auth ./hcp-auth
COPY hcp-gateway ./hcp-gateway
COPY hcp-visual ./hcp-visual
COPY hcp-modules ./hcp-modules
COPY hcp-demo ./hcp-demo
COPY hcp-register ./hcp-register
COPY hcp-common ./hcp-common
COPY hcp-api ./hcp-api

# Build all modules except those with Java 8 dependencies or resource issues
# Skipped: hcp-demo (resource issues), hcp-register (resource issues),
# hcp-file, hcp-job, hcp-operator, hcp-mp, hcp-simulator (jdk.tools dependency)
RUN mvn clean install -DskipTests -B -pl '!hcp-visual,!hcp-demo,!hcp-register,!hcp-modules/hcp-system,!hcp-modules/hcp-gen,!hcp-modules/hcp-file,!hcp-modules/hcp-job,!hcp-modules/hcp-operator,!hcp-modules/hcp-mp,!hcp-modules/hcp-simulator'

# Build the gateway module specifically
RUN cd hcp-gateway && mvn clean package -DskipTests -B

# Copy JAR to the expected location
RUN cp /app/hcp-gateway/target/hcp-gateway.jar /app/target.jar

# ===================================================================

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine

# Set working directory
WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/target.jar app.jar

# Expose port
EXPOSE 38080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:38080/actuator/health || exit 1

# Run the application
CMD ["java", "-jar", "app.jar"]