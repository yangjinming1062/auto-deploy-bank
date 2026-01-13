# Stage 1: Build the application with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app
COPY . .
RUN chmod +x ./mvnw
RUN ./mvnw clean package -pl ors-api -am -DskipTests -B

# Stage 2: Create the final lightweight image
FROM eclipse-temurin:17-jre-alpine

# Create a non-root user and group
RUN addgroup -S ors && adduser -S ors -G ors

# Create necessary directories
RUN mkdir -p /app/config /app/files /app/logs /app/graphs /app/elevation_cache && \
    chown -R ors:ors /app

USER ors
WORKDIR /app

# Copy the application JAR from the builder stage
COPY --chown=ors:ors --from=builder /app/ors-api/target/ors.jar /app/target.jar

# Copy configuration and data files
COPY --chown=ors:ors ors-config.yml ./config/
COPY --chown=ors:ors ors-api/src/test/files/heidelberg.test.pbf ./files/heidelberg.test.pbf

EXPOSE 8082

# Healthcheck to verify the service is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=300s --retries=5 CMD wget -q --spider http://localhost:8082/ors/v2/health || exit 1

CMD ["java", "-jar", "/app/target.jar"]
