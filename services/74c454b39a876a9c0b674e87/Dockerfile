# Multi-stage build for Spring Boot application
# Stage 1: Builder with Maven and JDK
FROM maven:3.6-openjdk-8 AS builder

WORKDIR /app

# Copy pom.xml and download dependencies
COPY backend/pom.xml ./backend/pom.xml
RUN cd backend && mvn dependency:go-offline -B

# Copy source code and build
COPY backend/src ./backend/src
RUN cd backend && mvn clean package -DskipTests -B

# Stage 2: Runtime image with JRE only
FROM adoptopenjdk:8-jre-hotspot

WORKDIR /app

# Copy JAR from builder stage
COPY --from=builder /app/backend/target/*.jar target.jar

# Expose the application port
EXPOSE 5432

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:5432/actuator/health || exit 1

# Run the application in foreground
CMD ["java", "-jar", "target.jar"]