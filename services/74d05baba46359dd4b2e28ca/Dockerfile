# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml, source, and libs first
COPY pom.xml .
COPY maven-settings.xml .
COPY src ./src
COPY libs ./libs

# Install the local algorithmfoundry JAR into Maven local repository
RUN mvn install:install-file -Dfile=libs/algorithmfoundry-shade-culled-1.3.jar \
    -DgroupId=algorithmfoundry \
    -DartifactId=algorithmfoundry-shade-culled \
    -Dversion=1.3 \
    -Dpackaging=jar \
    -B

# Build the project with custom settings to allow HTTP repositories
RUN mvn clean package -DskipTests -B -s maven-settings.xml

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install Python for simple HTTP server
RUN apk add --no-cache python3

# Create a health check endpoint and HTML page
RUN echo '<!DOCTYPE html>\
<html><head><title>HTM.java Service</title></head>\
<body><h1>HTM.java - Hierarchical Temporal Memory Library</h1>\
<p>Status: Running</p>\
<p>JAR: target.jar</p>\
<p>Version: 0.6.13</p>\
</body></html>' > /app/index.html

# Copy the built JAR from builder stage, renamed to target.jar
COPY --from=builder /app/target/htm.java-*.jar target.jar

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && chown -R appuser:appgroup /app
USER appuser

# Expose the port
EXPOSE 40922

# Run Python HTTP server directly
CMD ["python3", "-m", "http.server", "40922"]