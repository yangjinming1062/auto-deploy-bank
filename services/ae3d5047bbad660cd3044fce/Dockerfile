# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy only the necessary modules for building 07-boot-web
# Root pom.xml (will be modified to remove problematic modules)
COPY pom.xml ./

# Remove the <modules> section from root pom.xml to avoid Maven
# trying to resolve non-existent child modules
RUN sed -i '/<modules>/,/<\/modules>/d' pom.xml

# 07-boot parent module
COPY 07-boot/pom.xml ./07-boot/

# 07-boot-web module (the one we want to build)
COPY 07-boot/07-boot-web ./07-boot/07-boot-web

# Build only the 07-boot-web module (skip tests)
RUN mvn -f /app/07-boot/07-boot-web/pom.xml clean package -DskipTests -B

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# Install curl for healthcheck
RUN apk add --no-cache curl ca-certificates

WORKDIR /app

# Copy the built JAR from builder stage
# The JAR file naming pattern: artifactId-version-SNAPSHOT.jar
# Copy to app.jar for running and target.jar for volume mount/security scanning
COPY --from=builder /app/07-boot/07-boot-web/target/07-boot-web-*.jar /app/target.jar
COPY --from=builder /app/07-boot/07-boot-web/target/07-boot-web-*.jar app.jar

# Expose the application port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]