# Multi-stage build for Glowroot Central
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Create user
RUN useradd --no-log-init -r -g root glowroot

# Install unzip for extracting WAR
RUN apt-get update && apt-get install -y unzip && rm -rf /var/lib/apt/lists/*

# Copy pom.xml first for dependency caching
COPY pom.xml .

# Copy all source code
COPY agent agent
COPY central central
COPY common common
COPY common2 common2
COPY wire-api wire-api
COPY ui ui
COPY build build
COPY webdriver-tests webdriver-tests

# Build the application
RUN mvn clean package -DskipTests -B

# Extract the WAR file to get lib jars and properties
WORKDIR /build/central
RUN unzip -q target/glowroot-central-*.war -d temp \
    && cp temp/WEB-INF/lib/*.jar /build/ 2>/dev/null || true \
    && cp temp/META-INF/glowroot-central.properties /build/ \
    && rm -rf temp

# Find and copy the main JAR, and create target.jar for security scanning
RUN find /build/central/target -name "glowroot-central-*.jar" | head -1 | xargs -I {} cp {} /build/glowroot-central.jar && cp /build/glowroot-central.jar /build/target.jar

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# Install bash and wget for healthcheck
RUN apk add --no-cache bash wget

# Create user and directory structure
RUN addgroup -g 1000 glowroot && adduser -D -u 1000 -G glowroot glowroot && \
    mkdir -p /app/lib && chown -R glowroot:glowroot /app

# Copy scripts from builder
COPY --from=builder /build/central/docker-entrypoint.sh /usr/local/bin/
COPY --from=builder /build/central/glowroot-central.sh /usr/local/bin/

# Copy application files
WORKDIR /app
COPY --from=builder /build/glowroot-central.jar /app/glowroot-central.jar
COPY --from=builder /build/target.jar /app/target.jar
COPY --from=builder /build/glowroot-central.properties /app/
COPY --from=builder /build/*.jar /app/lib/

# List files for debugging
RUN ls -la /app/ && ls -la /app/lib/

# Set permissions
RUN chmod +x /usr/local/bin/docker-entrypoint.sh \
    && chmod +x /usr/local/bin/glowroot-central.sh

EXPOSE 4000 8181

USER glowroot

ENV GLOWROOT_OPTS=""

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["glowroot-central.sh"]