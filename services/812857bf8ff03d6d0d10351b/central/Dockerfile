# Multi-stage build for Glowroot Central
# Stage 1: Build with Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build

# Create user
RUN useradd --no-log-init -r -g root glowroot

# Copy source code
COPY agent agent
COPY central central
COPY common common
COPY common2 common2
COPY wire-api wire-api
COPY ui ui
COPY build build
COPY webdriver-tests webdriver-tests
COPY pom.xml pom.xml

# Build the application
RUN mvn clean package -DskipTests -B

# Extract the WAR file
WORKDIR /build/central
RUN unzip -q target/glowroot-central-*.war -d temp \
    && cp temp/WEB-INF/classes/glowroot-central.properties /build/ \
    && cp temp/WEB-INF/lib/*.jar /build/ 2>/dev/null || true \
    && cp temp/WEB-INF/classes/*.jar /build/ 2>/dev/null || true \
    && rm -rf temp

# Find and rename the main JAR, and create target.jar for security scanning
RUN find /build/target -name "glowroot-central-*.jar" | head -1 | xargs -I {} cp {} /build/glowroot-central.jar && cp /build/glowroot-central.jar /build/target.jar

# Stage 2: Runtime image
FROM eclipse-temurin:17-jre-alpine

# Install bash
RUN apk add --no-cache bash

# Create user
RUN addgroup -g 1000 glowroot && adduser -D -u 1000 -G glowroot glowroot

# Copy scripts from builder stage
COPY --from=0 /build/central/docker-entrypoint.sh /usr/local/bin/
COPY --from=0 /build/central/glowroot-central.sh /usr/local/bin/

# Copy application files
WORKDIR /app
COPY --from=0 /build/glowroot-central.jar /app/
COPY --from=0 /build/target.jar /app/
COPY --from=0 /build/glowroot-central.properties /app/

# Set permissions
RUN chmod +x /usr/local/bin/docker-entrypoint.sh \
    && chmod +x /usr/local/bin/glowroot-central.sh \
    && chown -R glowroot:glowroot /app

EXPOSE 4000 8181

USER glowroot

ENV GLOWROOT_OPTS=""

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["glowroot-central.sh"]