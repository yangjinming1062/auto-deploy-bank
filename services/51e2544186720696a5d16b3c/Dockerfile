# Multi-stage build for jBPM Service
# Stage 1: Build the Spring Boot application
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml and resolve dependencies
COPY jbpm-service/pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY jbpm-service/src ./src

# Build the application
RUN mvn -f pom.xml clean package -DskipTests -B

# Stage 2: Runtime stage
FROM eclipse-temurin:17-jre-alpine AS runtime

WORKDIR /app

# Copy the built JAR from builder stage
COPY --from=builder /app/target/*.jar target.jar

# Copy configuration files
COPY datasource.properties ./
COPY userinfo.properties ./
COPY usergroups.properties ./
COPY jbpm.usergroup.callback.properties ./
COPY jboss-ejb-client.properties ./

# Expose port
EXPOSE 40158

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:40158/actuator/health || exit 1

# Run the application
CMD ["java", "-jar", "target.jar"]